#!/usr/bin/env node

const chromeEndpoint = process.argv[2] || 'http://127.0.0.1:9224';
const explorerUrl = process.argv[3] || 'http://127.0.0.1:5176/explore';
const timeoutMs = Number(process.argv[4] || 90000);

async function createTarget() {
  const response = await fetch(`${chromeEndpoint}/json/new?about:blank`, { method: 'PUT' });
  if (!response.ok) throw new Error(`Unable to create Chrome target: HTTP ${response.status}`);
  return response.json();
}

const target = await createTarget();
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  ws.onopen = resolve;
  ws.onerror = reject;
});

let nextId = 1;
const pending = new Map();
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (!message.id || !pending.has(message.id)) return;
  const { resolve, reject } = pending.get(message.id);
  pending.delete(message.id);
  if (message.error) reject(new Error(JSON.stringify(message.error)));
  else resolve(message.result);
};

function send(method, params = {}) {
  const id = nextId++;
  ws.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

async function evaluate(expression, awaitPromise = false) {
  const result = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise });
  if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
  return result.result.value;
}

await send('Page.enable');
await send('Runtime.enable');
await send('Performance.enable');
await send('Page.addScriptToEvaluateOnNewDocument', {
  source: `
window.__vitruviusLongTasks = [];
try {
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      window.__vitruviusLongTasks.push({ name: entry.name, startTime: entry.startTime, duration: entry.duration });
    }
  }).observe({ type: 'longtask', buffered: true });
} catch (_) {}
`,
});

await send('Page.navigate', { url: explorerUrl });

const startedAt = Date.now();
while (Date.now() - startedAt < timeoutMs) {
  const ready = await evaluate(`(() => {
    const metrics = window.__vitruviusGraphRenderMetrics || [];
    return Boolean(metrics.find((metric) => metric.phase === 'loadGraph:networkCreated'));
  })()`);
  if (ready) break;
  await new Promise((resolve) => setTimeout(resolve, 500));
}

await new Promise((resolve) => setTimeout(resolve, 3000));

const summary = await evaluate(`(() => {
  const metrics = window.__vitruviusGraphRenderMetrics || [];
  const resources = performance.getEntriesByType('resource')
    .filter((entry) => String(entry.name).includes('/perspective/aec-mepfs/nodes'))
    .map((entry) => ({
      name: entry.name,
      startTime: entry.startTime,
      duration: entry.duration,
      transferSize: entry.transferSize,
      encodedBodySize: entry.encodedBodySize,
      decodedBodySize: entry.decodedBodySize,
    }));
  const paints = performance.getEntriesByType('paint').map((entry) => ({ name: entry.name, startTime: entry.startTime }));
  const longTasks = window.__vitruviusLongTasks || [];
  return {
    url: location.href,
    title: document.title,
    metrics,
    resources,
    paints,
    longTaskCount: longTasks.length,
    longTaskTotalMs: longTasks.reduce((sum, task) => sum + task.duration, 0),
    longTaskMaxMs: longTasks.reduce((max, task) => Math.max(max, task.duration), 0),
    longTasksTop5: longTasks.slice().sort((a, b) => b.duration - a.duration).slice(0, 5),
    memory: performance.memory ? {
      usedJSHeapSize: performance.memory.usedJSHeapSize,
      totalJSHeapSize: performance.memory.totalJSHeapSize,
      jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
    } : null,
    canvasCount: document.querySelectorAll('canvas').length,
    bodyText: document.body?.innerText?.slice(0, 1200) || '',
  };
})()`);

console.log(JSON.stringify(summary, null, 2));
ws.close();
