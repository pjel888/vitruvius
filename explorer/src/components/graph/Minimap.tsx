import { useCallback, useEffect, useRef } from 'react';
import type { GraphController } from './VisNetworkHost';

interface MinimapProps {
  controllerRef: React.RefObject<GraphController | null>;
}

const TYPE_COLORS: Record<string, string> = {
  taxonomy: '#60a5fa',
  topic: '#818cf8',
  subtopic: '#c084fc',
  concept: '#a78bfa',
  rule: '#f87171',
  definition: '#34d399',
  procedure: '#fbbf24',
  exception: '#f472b6',
  evidence_span: '#38bdf8',
};

type OverviewSnapshot = ReturnType<GraphController['getOverviewSnapshot']>;

function getSnapshotTransform(snapshot: OverviewSnapshot, canvas: HTMLCanvasElement) {
  const xs = snapshot.nodes.map((node) => node.x);
  const ys = snapshot.nodes.map((node) => node.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const width = Math.max(maxX - minX, 1);
  const height = Math.max(maxY - minY, 1);
  const padding = 12;
  const scale = Math.min((canvas.width - padding * 2) / width, (canvas.height - padding * 2) / height);
  const offsetX = (canvas.width - width * scale) / 2;
  const offsetY = (canvas.height - height * scale) / 2;
  return { minX, minY, scale, offsetX, offsetY };
}

export default function Minimap({ controllerRef }: MinimapProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const lastDrawnVersionRef = useRef<number>(-1);
  const draggingRef = useRef(false);

  const drawSnapshot = useCallback((ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, '#0d1a24');
    gradient.addColorStop(1, '#061016');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const snapshot = controllerRef.current?.getOverviewSnapshot();
    if (!snapshot || snapshot.nodes.length === 0) {
      ctx.fillStyle = '#39d5c8';
      ctx.font = '10px Avenir Next, sans-serif';
      ctx.fillText('Waiting for graph', 12, canvas.height / 2);
      return;
    }

    const { minX, minY, scale, offsetX, offsetY } = getSnapshotTransform(snapshot, canvas);

    snapshot.nodes.forEach((node) => {
      ctx.fillStyle = TYPE_COLORS[node.type] || '#a78bfa';
      ctx.beginPath();
      ctx.arc(offsetX + (node.x - minX) * scale, offsetY + (node.y - minY) * scale, 1.9, 0, Math.PI * 2);
      ctx.fill();
    });

    const viewportWidth = Math.max(10, snapshot.viewport.width * scale);
    const viewportHeight = Math.max(8, snapshot.viewport.height * scale);
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 1.5;
    const cameraX = offsetX + (snapshot.camera.x - minX) * scale;
    const cameraY = offsetY + (snapshot.camera.y - minY) * scale;
    ctx.strokeRect(cameraX - viewportWidth / 2, cameraY - viewportHeight / 2, viewportWidth, viewportHeight);
    ctx.fillStyle = 'rgba(251, 191, 36, 0.08)';
    ctx.fillRect(cameraX - viewportWidth / 2, cameraY - viewportHeight / 2, viewportWidth, viewportHeight);
  }, [controllerRef]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const minimapCanvas: HTMLCanvasElement = canvas;
    const context = canvas.getContext('2d');
    if (context === null) return;
    const drawContext: CanvasRenderingContext2D = context;

    function maybeDraw(force = false) {
      const nextVersion = controllerRef.current?.getOverviewVersion() ?? 0;
      if (!force && nextVersion === lastDrawnVersionRef.current) return;
      drawSnapshot(drawContext, minimapCanvas);
      lastDrawnVersionRef.current = nextVersion;
    }

    maybeDraw(true);
    const intervalId = window.setInterval(() => maybeDraw(false), 150);

    return () => {
      window.clearInterval(intervalId);
    };
  }, [controllerRef, drawSnapshot]);

  function centerFromPointer(event: React.PointerEvent<HTMLCanvasElement>) {
    const canvas = canvasRef.current;
    if (!canvas || !controllerRef.current) return;
    const snapshot = controllerRef.current.getOverviewSnapshot();
    if (snapshot.nodes.length === 0) return;

    const { minX, minY, scale, offsetX, offsetY } = getSnapshotTransform(snapshot, canvas);
    const rect = canvas.getBoundingClientRect();
    const localX = (event.clientX - rect.left) * (canvas.width / rect.width);
    const localY = (event.clientY - rect.top) * (canvas.height / rect.height);
    const worldX = (localX - offsetX) / scale + minX;
    const worldY = (localY - offsetY) / scale + minY;
    controllerRef.current.centerOnPosition(worldX, worldY);
    lastDrawnVersionRef.current = -1;
  }

  return (
    <div className="kg-card h-36 w-48 overflow-hidden rounded-2xl p-2">
      <div className="mb-1 flex items-center justify-between px-1 text-[10px] uppercase tracking-[0.24em] text-text-dim">
        <span>Minimap</span>
        <span>drag</span>
      </div>
      <canvas
        ref={canvasRef}
        width={176}
        height={112}
        role="button"
        tabIndex={0}
        aria-label="Graph minimap. Click or drag to pan the graph viewport."
        className="h-28 w-full cursor-grab rounded-xl border border-border bg-bg active:cursor-grabbing"
        onPointerDown={(event) => {
          draggingRef.current = true;
          event.currentTarget.setPointerCapture(event.pointerId);
          centerFromPointer(event);
        }}
        onPointerMove={(event) => {
          if (draggingRef.current) centerFromPointer(event);
        }}
        onPointerUp={(event) => {
          draggingRef.current = false;
          event.currentTarget.releasePointerCapture(event.pointerId);
        }}
        onPointerCancel={() => {
          draggingRef.current = false;
        }}
        onKeyDown={(event) => {
          if (event.key === 'Enter' || event.key === ' ') {
            controllerRef.current?.fitView();
          }
        }}
      />
    </div>
  );
}
