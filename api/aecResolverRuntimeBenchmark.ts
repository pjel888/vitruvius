import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_SCHEMA_VERSION = 'aec-mepfs-resolver-runtime-benchmark/v1';
export const AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_REPORT_FILENAME = 'runtime-resolver-benchmark-report.json';
export const AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_DIR = '006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark';
export const AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_DISPOSITION = 'observational_default_off_route_harness_no_threshold_claim';

const RUNTIME_FLAG = 'VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME';
const FIXTURE_FLAG = 'VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH';
const RUN_ID_RE = /^[A-Za-z0-9_.-]+$/;
const DEFAULT_REPETITIONS = 5;
const DEFAULT_WARMUP = 1;
const PLANNED_THRESHOLDS = [
  'resolver exact ID lookup p95 <= 100 ms',
  'resolver context resolve p95 <= 250 ms',
] as const;

const API_DIR = dirname(fileURLToPath(import.meta.url));
const DEFAULT_REPO_ROOT = resolve(API_DIR, '..');

let importCounter = 0;

type HonoLikeApi = {
  fetch(request: Request): Promise<Response>;
};

type BenchmarkOperation = {
  name: string;
  ok: boolean;
  repetitions: number;
  warmup: number;
  durationsMs: number[];
  p50Ms: number;
  p95Ms: number;
  errors: string[];
};

type BenchmarkOptions = {
  runId?: string;
  repoRoot?: string;
  outputPath?: string;
  repetitions?: number;
  warmup?: number;
};

type BenchmarkReport = {
  schemaVersion: string;
  ok: boolean;
  runId: string;
  startedAtUtc: string;
  finishedAtUtc: string;
  reportPath: string;
  fixturePath: string;
  benchmarkScope: Record<string, boolean>;
  runtimeThresholdEvidence: {
    evaluated: false;
    disposition: string;
    passFailClaim: false;
    plannedThresholds: string[];
  };
  environment: Record<string, string | number | null>;
  plan: {
    repetitions: number;
    warmup: number;
    percentiles: string[];
    corpus: string;
  };
  operations: BenchmarkOperation[];
  operationCoverage: {
    requiredOperations: string[];
    operationsTotal: number;
    operationsPassed: number;
    missingRequiredOperations: string[];
    unexpectedOperations: string[];
    allRequiredOperationsPresent: boolean;
    allOperationsOk: boolean;
  };
  safetyInvariants: Record<string, boolean>;
  errors: string[];
  warnings: string[];
};

const REQUIRED_OPERATIONS = [
  'default_off_resolve_absent',
  'enabled_single_value_resolve',
  'enabled_composed_resolve',
  'enabled_conflict_resolve',
  'enabled_none_resolve',
  'enabled_trace_lookup',
] as const;

function resolverRequest(assetContext = 'public_building', text = 'Resolve accessibility overlay for a public building entrance.') {
  return {
    query: {
      concept_id: 'VTN-CON-0000002',
      asset_context: assetContext,
      text,
      context_ids: ['VTN-DOM-0000001'],
      jurisdiction_filters: ['PH'],
      discipline_filters: ['architecture'],
      trace_requested: true,
    },
    jurisdiction: 'PH',
    effective_date: '2026-04-25',
  };
}

function domainRequest() {
  return {
    query: {
      text: 'Resolve the Architecture backbone domain.',
      trace_requested: true,
    },
  };
}

function composedRequest() {
  return resolverRequest(
    'national_and_local_compatible',
    'Resolve compatible national and local accessibility requirements.',
  );
}

function conflictRequest() {
  return {
    ...resolverRequest(
      'equal_force_incompatible',
      'Resolve equal-force incompatible accessibility requirements.',
    ),
    jurisdiction: 'PH-EXAMPLE-LGU',
  };
}

function noneRequest() {
  return {
    ...resolverRequest(
      'no_overlay',
      'Resolve an unmodeled local accessibility overlay.',
    ),
    jurisdiction: 'PH-UNMODELED',
  };
}

export async function runAecMepfsResolverRuntimeBenchmark(options: BenchmarkOptions = {}): Promise<BenchmarkReport> {
  const runId = sanitizeRunId(options.runId);
  const repoRoot = resolve(options.repoRoot || DEFAULT_REPO_ROOT);
  const outputPath = resolveBenchmarkReportPath(repoRoot, runId, options.outputPath);
  const repetitions = sanitizePositiveInteger(options.repetitions, DEFAULT_REPETITIONS, 'repetitions');
  const warmup = sanitizeNonNegativeInteger(options.warmup, DEFAULT_WARMUP, 'warmup');
  const startedAtUtc = utcNow();
  const originalRuntimeFlag = process.env[RUNTIME_FLAG];
  const originalFixtureFlag = process.env[FIXTURE_FLAG];
  const warnings: string[] = [];
  const errors: string[] = [];
  let operations: BenchmarkOperation[] = [];

  try {
    const defaultOffApi = await importDefaultOffApi();
    const enabledApi = await importEnabledApi();

    operations = [
      await measureOperation('default_off_resolve_absent', repetitions, warmup, async () => {
        const response = await defaultOffApi.fetch(new Request('http://localhost/v2/resolve', {
          method: 'POST',
          body: JSON.stringify(resolverRequest()),
          headers: { 'content-type': 'application/json' },
        }));
        if (response.status !== 404) {
          throw new Error(`expected default-off /v2/resolve status 404, received ${response.status}`);
        }
      }),
      await measureOperation('enabled_single_value_resolve', repetitions, warmup, async () => {
        await expectResolveResult(enabledApi, resolverRequest(), 'single_value');
      }),
      await measureOperation('enabled_composed_resolve', repetitions, warmup, async () => {
        await expectResolveResult(enabledApi, composedRequest(), 'composed');
      }),
      await measureOperation('enabled_conflict_resolve', repetitions, warmup, async () => {
        await expectResolveResult(enabledApi, conflictRequest(), 'conflict');
      }),
      await measureOperation('enabled_none_resolve', repetitions, warmup, async () => {
        await expectResolveResult(enabledApi, noneRequest(), 'none');
      }),
      await measureOperation('enabled_trace_lookup', repetitions, warmup, async () => {
        const payload = await expectResolveResult(enabledApi, domainRequest(), 'single_value');
        const traceResponse = await enabledApi.fetch(
          new Request(`http://localhost/v2/resolve/trace/${encodeURIComponent(String(payload.traceId))}`),
        );
        if (traceResponse.status !== 200) {
          throw new Error(`expected trace status 200, received ${traceResponse.status}`);
        }
        const tracePayload = await traceResponse.json() as Record<string, unknown>;
        if (tracePayload.traceId !== payload.traceId) {
          throw new Error('trace lookup returned a mismatched trace id');
        }
      }),
    ];
  } catch (error: any) {
    errors.push(error?.message || String(error));
  } finally {
    restoreEnv(RUNTIME_FLAG, originalRuntimeFlag);
    restoreEnv(FIXTURE_FLAG, originalFixtureFlag);
  }

  for (const operation of operations) {
    errors.push(...operation.errors);
  }
  const operationCoverage = summarizeOperationCoverage(operations);
  if (!operationCoverage.allRequiredOperationsPresent) {
    errors.push(`missing required operations: ${operationCoverage.missingRequiredOperations.join(', ')}`);
  }
  if (operationCoverage.unexpectedOperations.length > 0) {
    errors.push(`unexpected operations: ${operationCoverage.unexpectedOperations.join(', ')}`);
  }

  const finishedAtUtc = utcNow();
  const safetyInvariants = {
    defaultOffRouteAbsentOnDefaultImport: operations.find((operation) => operation.name === 'default_off_resolve_absent')?.ok === true,
    guardedFlagRequired: true,
    defaultOnFeatureFlag: false,
    fileBackedOnly: true,
    protectedContentIngest: false,
    liveNeo4jWrites: false,
    kgRebuild: false,
    explorerDefaultAdoption: false,
    externalApiServerNetworkCalls: false,
    runtimeThresholdsEvaluated: false,
    runtimeThresholdClaim: false,
  };
  const report: BenchmarkReport = {
    schemaVersion: AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_SCHEMA_VERSION,
    ok: errors.length === 0 && operations.every((operation) => operation.ok),
    runId,
    startedAtUtc,
    finishedAtUtc,
    reportPath: relativePath(repoRoot, outputPath),
    fixturePath: relativePath(repoRoot, resolve(repoRoot, 'scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json')),
    benchmarkScope: {
      defaultOffResolverRouteInvocation: true,
      inProcessHonoFetch: true,
      externalApiServerNetworkCalls: false,
      neo4jQueries: false,
      kgRebuild: false,
      protectedContentIngest: false,
      explorerRuntimeCalls: false,
      featureFlagCutover: false,
      runtimeThresholdsEvaluated: false,
    },
    runtimeThresholdEvidence: {
      evaluated: false,
      disposition: AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_DISPOSITION,
      passFailClaim: false,
      plannedThresholds: [...PLANNED_THRESHOLDS],
    },
    environment: {
      bunVersion: typeof Bun !== 'undefined' ? Bun.version : null,
      platform: process.platform,
      arch: process.arch,
      nodeVersion: process.version,
      cpuCount: typeof navigator !== 'undefined' ? navigator.hardwareConcurrency : null,
    },
    plan: {
      repetitions,
      warmup,
      percentiles: ['p50', 'p95'],
      corpus: 'non-protected resolver golden fixtures in scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json',
    },
    operations,
    operationCoverage,
    safetyInvariants,
    errors: [...new Set(errors)].sort(),
    warnings: [...new Set(warnings)].sort(),
  };

  writeReport(outputPath, report);
  return report;
}

async function importDefaultOffApi(): Promise<HonoLikeApi> {
  delete process.env[RUNTIME_FLAG];
  const module = await import(`./index.ts?resolver-benchmark-default-off=${Date.now()}-${importCounter++}`);
  return module.default as HonoLikeApi;
}

async function importEnabledApi(): Promise<HonoLikeApi> {
  process.env[RUNTIME_FLAG] = 'true';
  const module = await import(`./index.ts?resolver-benchmark-enabled=${Date.now()}-${importCounter++}`);
  return module.default as HonoLikeApi;
}

async function expectResolveResult(api: HonoLikeApi, requestPayload: Record<string, unknown>, expectedResultType: string) {
  const response = await api.fetch(new Request('http://localhost/v2/resolve', {
    method: 'POST',
    body: JSON.stringify(requestPayload),
    headers: { 'content-type': 'application/json' },
  }));
  if (response.status !== 200) {
    throw new Error(`expected /v2/resolve status 200, received ${response.status}`);
  }
  const payload = await response.json() as Record<string, any>;
  if (payload.resultType !== expectedResultType) {
    throw new Error(`expected resultType ${expectedResultType}, received ${payload.resultType}`);
  }
  if (payload.boundaries?.liveNeo4jWrites !== false || payload.boundaries?.kgRebuild !== false) {
    throw new Error('resolver response crossed Neo4j/KG rebuild safety boundary');
  }
  if (payload.boundaries?.protectedContentIngest !== false) {
    throw new Error('resolver response crossed protected content safety boundary');
  }
  return payload;
}

async function measureOperation(
  name: string,
  repetitions: number,
  warmup: number,
  operation: () => Promise<void>,
): Promise<BenchmarkOperation> {
  const errors: string[] = [];
  for (let index = 0; index < warmup; index += 1) {
    try {
      await operation();
    } catch (error: any) {
      errors.push(`${name}.warmup[${index + 1}]: ${error?.message || String(error)}`);
      break;
    }
  }
  const durationsMs: number[] = [];
  if (errors.length === 0) {
    for (let index = 0; index < repetitions; index += 1) {
      const start = performance.now();
      try {
        await operation();
      } catch (error: any) {
        errors.push(`${name}[${index + 1}]: ${error?.message || String(error)}`);
      } finally {
        durationsMs.push(Math.max(0, performance.now() - start));
      }
      if (errors.length > 0) {
        break;
      }
    }
  }
  return {
    name,
    ok: errors.length === 0,
    repetitions: durationsMs.length,
    warmup,
    durationsMs: durationsMs.map((value) => round(value)),
    p50Ms: round(percentile(durationsMs, 50)),
    p95Ms: round(percentile(durationsMs, 95)),
    errors,
  };
}

function summarizeOperationCoverage(operations: BenchmarkOperation[]) {
  const names = operations.map((operation) => operation.name);
  const missingRequiredOperations = REQUIRED_OPERATIONS.filter((name) => !names.includes(name));
  const unexpectedOperations = names.filter((name) => !(REQUIRED_OPERATIONS as readonly string[]).includes(name));
  const operationsPassed = operations.filter((operation) => operation.ok).length;
  return {
    requiredOperations: [...REQUIRED_OPERATIONS],
    operationsTotal: operations.length,
    operationsPassed,
    missingRequiredOperations,
    unexpectedOperations,
    allRequiredOperationsPresent: missingRequiredOperations.length === 0,
    allOperationsOk: operationsPassed === operations.length && missingRequiredOperations.length === 0 && unexpectedOperations.length === 0,
  };
}

function resolveBenchmarkReportPath(repoRoot: string, runId: string, outputPath?: string) {
  const candidate = outputPath
    ? resolve(outputPath)
    : resolve(repoRoot, AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_DIR, runId, AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_REPORT_FILENAME);
  const allowedRoot = resolve(repoRoot, AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_DIR);
  const relativeToAllowedRoot = relative(allowedRoot, candidate).split('\\').join('/');
  if (relativeToAllowedRoot === '' || relativeToAllowedRoot.startsWith('../') || relativeToAllowedRoot === '..') {
    throw new Error('runtime resolver benchmark report path must stay inside the benchmark evidence directory');
  }
  const relativeParts = relativeToAllowedRoot.split('/');
  if (relativeParts.length !== 2 || relativeParts[0] !== runId || relativeParts[1] !== AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_REPORT_FILENAME) {
    throw new Error(`runtime resolver benchmark report path must be scoped to ${runId}/${AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_REPORT_FILENAME}`);
  }
  return candidate;
}

function sanitizeRunId(value?: string) {
  const candidate = value || new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}Z$/, 'Z');
  if (!RUN_ID_RE.test(candidate)) {
    throw new Error('run id must contain only letters, digits, underscore, dot, or dash');
  }
  return candidate;
}

function sanitizePositiveInteger(value: unknown, fallback: number, label: string) {
  const parsed = value === undefined ? fallback : Number(value);
  if (!Number.isInteger(parsed) || parsed < 1) {
    throw new Error(`${label} must be a positive integer`);
  }
  return parsed;
}

function sanitizeNonNegativeInteger(value: unknown, fallback: number, label: string) {
  const parsed = value === undefined ? fallback : Number(value);
  if (!Number.isInteger(parsed) || parsed < 0) {
    throw new Error(`${label} must be a non-negative integer`);
  }
  return parsed;
}

function percentile(values: number[], percentileValue: number) {
  if (values.length === 0) {
    return 0;
  }
  const ordered = [...values].sort((left, right) => left - right);
  const index = Math.max(0, Math.min(ordered.length - 1, Math.ceil((percentileValue / 100) * ordered.length) - 1));
  return ordered[index];
}

function round(value: number) {
  return Math.round(value * 1000) / 1000;
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

function relativePath(repoRoot: string, path: string) {
  return relative(repoRoot, path).split('\\').join('/');
}

function writeReport(path: string, report: BenchmarkReport) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(report, null, 2)}\n`, 'utf-8');
}

function restoreEnv(name: string, value: string | undefined) {
  if (value === undefined) {
    delete process.env[name];
  } else {
    process.env[name] = value;
  }
}

function parseCliArgs(argv: string[]) {
  const options: BenchmarkOptions = {};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];
    if (arg === '--run-id') {
      options.runId = next;
      index += 1;
    } else if (arg === '--repo-root') {
      options.repoRoot = next;
      index += 1;
    } else if (arg === '--output') {
      options.outputPath = next;
      index += 1;
    } else if (arg === '--repetitions') {
      options.repetitions = Number(next);
      index += 1;
    } else if (arg === '--warmup') {
      options.warmup = Number(next);
      index += 1;
    } else if (arg === '--help' || arg === '-h') {
      printUsageAndExit(0);
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }
  return options;
}

function printUsageAndExit(code: number): never {
  console.log('Usage: bun aecResolverRuntimeBenchmark.ts [--run-id RUN_ID] [--repo-root PATH] [--output PATH] [--repetitions N] [--warmup N]');
  process.exit(code);
}

if (import.meta.main) {
  try {
    const report = await runAecMepfsResolverRuntimeBenchmark(parseCliArgs(Bun.argv.slice(2)));
    console.log(JSON.stringify(report, null, 2));
    process.exit(report.ok ? 0 : 1);
  } catch (error: any) {
    console.error(JSON.stringify({ ok: false, errors: [error?.message || String(error)] }, null, 2));
    process.exit(1);
  }
}
