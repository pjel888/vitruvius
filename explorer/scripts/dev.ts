import { join, resolve } from 'node:path';

const explorerRoot = resolve(import.meta.dir, '..');
const repoRoot = resolve(explorerRoot, '..');
const apiRoot = join(repoRoot, 'api');
const neo4jHttpUrl = 'http://localhost:7474';
const apiHealthUrl = 'http://localhost:3000/health';

function sleep(ms: number) {
  return new Promise((resolvePromise) => setTimeout(resolvePromise, ms));
}

async function canReach(url: string) {
  try {
    const response = await fetch(url);
    return response.ok;
  } catch {
    return false;
  }
}

function killProcessOnPort3000() {
  const result = Bun.spawnSync(['bash', '-lc', 'lsof -ti:3000 2>/dev/null || true'], {
    stdout: 'pipe',
    stderr: 'pipe',
  });

  const pid = result.stdout.toString().trim();
  if (!pid) return false;

  console.log('🧹 Cleaning up existing API on port 3000...');
  Bun.spawnSync(['kill', pid], {
    stdout: 'ignore',
    stderr: 'ignore',
  });
  return true;
}

async function waitForApiReady() {
  for (let attempt = 0; attempt < 30; attempt += 1) {
    if (await canReach(apiHealthUrl)) {
      return true;
    }
    await sleep(1000);
  }

  return false;
}

if (!(await canReach(neo4jHttpUrl))) {
  console.error('⚠️  Neo4j is not running. Start it with:');
  console.error('   brew services start neo4j');
  process.exit(1);
}

killProcessOnPort3000();

console.log('🚀 Starting Vitruvius Graph API on port 3000...');
const apiProcess = Bun.spawn(['bun', 'run', 'index.ts'], {
  cwd: apiRoot,
  env: {
    ...process.env,
    NEO4J_PASS: process.env.NEO4J_PASS || 'password',
  },
  stdout: 'inherit',
  stderr: 'inherit',
});

console.log('⏳ Waiting for API to start...');
const apiReady = await waitForApiReady();

if (!apiReady) {
  console.error('❌ API failed to become ready on http://localhost:3000/health');
  apiProcess.kill();
  process.exit(1);
}

console.log('✅ API ready!');
console.log('🌐 Starting Explorer dev server on port 5173...');

const viteProcess = Bun.spawn(['bun', 'run', 'dev:vite', '--host'], {
  cwd: explorerRoot,
  env: process.env,
  stdout: 'inherit',
  stderr: 'inherit',
});

let cleanedUp = false;

function cleanup(exitCode = 0) {
  if (cleanedUp) return;
  cleanedUp = true;

  if (viteProcess.exitCode === null) {
    viteProcess.kill();
  }

  if (apiProcess.exitCode === null) {
    console.log('🛑 Shutting down API...');
    apiProcess.kill();
  }

  process.exit(exitCode);
}

process.on('SIGINT', () => cleanup(130));
process.on('SIGTERM', () => cleanup(143));

const viteExitCode = await viteProcess.exited;
cleanup(viteExitCode ?? 0);
