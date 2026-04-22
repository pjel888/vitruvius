import { useEffect, useRef } from 'react';
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

export default function Minimap({ controllerRef }: MinimapProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const lastDrawnVersionRef = useRef<number>(-1);

  function drawSnapshot(ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) {
    ctx.fillStyle = '#16181f';
    ctx.fillRect(0, 0, 160, 120);

    const snapshot = controllerRef.current?.getOverviewSnapshot();
    if (!snapshot || snapshot.nodes.length === 0) {
      ctx.fillStyle = '#4fc1e9';
      ctx.font = '10px sans-serif';
      ctx.fillText('Minimap', 10, 60);
      return;
    }

    const xs = snapshot.nodes.map((node) => node.x);
    const ys = snapshot.nodes.map((node) => node.y);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);
    const width = Math.max(maxX - minX, 1);
    const height = Math.max(maxY - minY, 1);
    const scale = Math.min((canvas.width - 16) / width, (canvas.height - 16) / height);
    const offsetX = (canvas.width - width * scale) / 2;
    const offsetY = (canvas.height - height * scale) / 2;

    snapshot.nodes.forEach((node) => {
      ctx.fillStyle = TYPE_COLORS[node.type] || '#a78bfa';
      ctx.beginPath();
      ctx.arc(offsetX + (node.x - minX) * scale, offsetY + (node.y - minY) * scale, 2, 0, Math.PI * 2);
      ctx.fill();
    });

    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 1.5;
    const cameraX = offsetX + (snapshot.camera.x - minX) * scale;
    const cameraY = offsetY + (snapshot.camera.y - minY) * scale;
    ctx.strokeRect(cameraX - 10, cameraY - 8, 20, 16);
  }

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
  }, [controllerRef]);

  function handleClick(event: React.MouseEvent<HTMLCanvasElement>) {
    const canvas = canvasRef.current;
    if (!canvas || !controllerRef.current) return;
    const snapshot = controllerRef.current.getOverviewSnapshot();
    if (snapshot.nodes.length === 0) return;

    const xs = snapshot.nodes.map((node) => node.x);
    const ys = snapshot.nodes.map((node) => node.y);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);
    const width = Math.max(maxX - minX, 1);
    const height = Math.max(maxY - minY, 1);
    const scale = Math.min((canvas.width - 16) / width, (canvas.height - 16) / height);
    const offsetX = (canvas.width - width * scale) / 2;
    const offsetY = (canvas.height - height * scale) / 2;
    const rect = canvas.getBoundingClientRect();
    const localX = event.clientX - rect.left;
    const localY = event.clientY - rect.top;
    const worldX = (localX - offsetX) / scale + minX;
    const worldY = (localY - offsetY) / scale + minY;
    controllerRef.current.centerOnPosition(worldX, worldY);
    lastDrawnVersionRef.current = -1;
  }

  return (
    <div className="absolute bottom-14 right-4 w-40 h-32 bg-panel border border-border rounded-lg overflow-hidden z-20 shadow-lg">
      <canvas ref={canvasRef} width={160} height={120} className="w-full h-full cursor-pointer" onClick={handleClick} />
    </div>
  );
}
