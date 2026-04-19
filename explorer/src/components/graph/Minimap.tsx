import { useEffect, useRef } from 'react';
import type { GraphController } from './SigmaHost';

interface MinimapProps {
  controllerRef: React.RefObject<GraphController | null>;
}

export default function Minimap(_props: MinimapProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    function draw() {
      if (!ctx || !canvas) return;
      ctx.fillStyle = '#16181f';
      ctx.fillRect(0, 0, 160, 120);
      // Note: actual minimap rendering would need access to the sigma graph
      // For now, show a placeholder
      ctx.fillStyle = '#4fc1e9';
      ctx.font = '10px sans-serif';
      ctx.fillText('Minimap', 10, 60);
    }

    const raf = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(raf);
  }, []);

  return (
    <div className="absolute bottom-14 right-4 w-40 h-32 bg-panel border border-border rounded-lg overflow-hidden z-20 shadow-lg">
      <canvas ref={canvasRef} width={160} height={120} className="w-full h-full" />
    </div>
  );
}
