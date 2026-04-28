import { afterEach, describe, expect, test } from 'bun:test';
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_DISPOSITION,
  AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_REPORT_FILENAME,
  AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_SCHEMA_VERSION,
  runAecMepfsResolverRuntimeBenchmark,
} from './aecResolverRuntimeBenchmark';

const ORIGINAL_RESOLVER_FLAG = process.env.VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME;
const ORIGINAL_FIXTURE_PATH = process.env.VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH;

afterEach(() => {
  restoreEnv('VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME', ORIGINAL_RESOLVER_FLAG);
  restoreEnv('VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH', ORIGINAL_FIXTURE_PATH);
});

function restoreEnv(name: string, value: string | undefined) {
  if (value === undefined) {
    delete process.env[name];
  } else {
    process.env[name] = value;
  }
}

function tempRepoRoot() {
  return mkdtempSync(join(tmpdir(), 'aec-resolver-runtime-benchmark-'));
}

describe('AEC-MEPFS default-on resolver runtime benchmark harness', () => {
  test('writes actual default-on in-process route metrics without source threshold claims', async () => {
    const repoRoot = tempRepoRoot();
    try {
      const report = await runAecMepfsResolverRuntimeBenchmark({
        repoRoot,
        runId: 'TEST_RUNTIME_BENCH',
        repetitions: 2,
        warmup: 1,
      });
      const reportPath = join(
        repoRoot,
        '006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/TEST_RUNTIME_BENCH',
        AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_REPORT_FILENAME,
      );
      const saved = JSON.parse(readFileSync(reportPath, 'utf-8'));

      expect(existsSync(reportPath)).toBe(true);
      expect(saved).toEqual(report);
      expect(report.ok).toBe(true);
      expect(report.schemaVersion).toBe(AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_SCHEMA_VERSION);
      expect(report.runtimeThresholdEvidence).toEqual({
        evaluated: false,
        disposition: AEC_MEPFS_RESOLVER_RUNTIME_BENCHMARK_DISPOSITION,
        passFailClaim: false,
        plannedThresholds: [
          'resolver exact ID lookup p95 <= 100 ms',
          'resolver context resolve p95 <= 250 ms',
        ],
      });
      expect(report.benchmarkScope).toMatchObject({
        defaultOnResolverRouteInvocation: true,
        disabledRollbackRouteAbsent: true,
        inProcessHonoFetch: true,
        externalApiServerNetworkCalls: false,
        neo4jQueries: false,
        kgRebuild: false,
        protectedContentIngest: false,
        explorerRuntimeCalls: false,
        featureFlagCutover: false,
        runtimeThresholdsEvaluated: false,
      });
      expect(report.safetyInvariants).toMatchObject({
        defaultOnRoutePresentOnDefaultImport: true,
        disabledRollbackRouteAbsent: true,
        guardedFlagRequired: false,
        hiddenDefaultOnFeatureFlag: false,
        explicitDefaultOnResolverPolicy: true,
        fileBackedOnly: true,
        protectedContentIngest: false,
        liveNeo4jWrites: false,
        kgRebuild: false,
        explorerDefaultAdoption: false,
        externalApiServerNetworkCalls: false,
        runtimeThresholdsEvaluated: false,
        runtimeThresholdClaim: false,
      });
      expect(report.operationCoverage).toMatchObject({
        operationsTotal: 6,
        operationsPassed: 6,
        missingRequiredOperations: [],
        unexpectedOperations: [],
        allRequiredOperationsPresent: true,
        allOperationsOk: true,
      });
      expect(report.operations.map((operation) => operation.name)).toEqual([
        'disabled_resolve_absent',
        'default_on_single_value_resolve',
        'default_on_composed_resolve',
        'default_on_conflict_resolve',
        'default_on_none_resolve',
        'default_on_trace_lookup',
      ]);
      expect(report.operations.every((operation) => operation.repetitions === 2)).toBe(true);
      expect(report.operations.every((operation) => operation.p95Ms >= 0)).toBe(true);
      expect(JSON.stringify(report)).not.toContain('official_url');
      expect(JSON.stringify(report)).not.toContain('blocking_notes');
    } finally {
      rmSync(repoRoot, { recursive: true, force: true });
    }
  });

  test('fences report output to the runtime-resolver-benchmark evidence directory', async () => {
    const repoRoot = tempRepoRoot();
    try {
      await expect(runAecMepfsResolverRuntimeBenchmark({
        repoRoot,
        runId: 'TEST_RUNTIME_BENCH',
        outputPath: join(repoRoot, 'outside.json'),
      })).rejects.toThrow('must stay inside the benchmark evidence directory');
    } finally {
      rmSync(repoRoot, { recursive: true, force: true });
    }
  });
});
