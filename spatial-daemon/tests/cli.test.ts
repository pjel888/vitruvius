import { describe, expect, it } from "vitest";
import { mkdtempSync, readFileSync, readdirSync, rmSync } from "fs";
import { tmpdir } from "os";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import { analyzeFromInputFile } from "../src/cli";
import { INTEGRITY_FOOTER_PREFIX } from "../src/contract_writer";
import type { SpatialEdge } from "../src/types";

const __dirname = dirname(fileURLToPath(import.meta.url));

function parseContractBody(raw: string): any {
  const footerIdx = raw.lastIndexOf("\n" + INTEGRITY_FOOTER_PREFIX);
  const body = footerIdx >= 0 ? raw.slice(0, footerIdx + 1) : raw;
  return JSON.parse(body);
}

describe("analyzeFromInputFile", () => {
  it("produces a valid spatial contract file from the box_intersection fixture", () => {
    const outDir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-out-"));
    try {
      const fixture = join(__dirname, "fixtures", "box_intersection.json");
      const result = analyzeFromInputFile(fixture, outDir);
      expect(result.writtenPath).toMatch(/spatial-smoke-01\.json$/);
      const files = readdirSync(outDir);
      expect(files).toContain("spatial-smoke-01.json");
      const payload = parseContractBody(readFileSync(result.writtenPath, "utf-8"));
      expect(payload.schema_version).toBe("1.0.0");
      expect(payload.instances).toHaveLength(2);
      // The two boxes overlap along x ∈ [5, 5.9]; expect a spatial_intersects edge
      const intersects = payload.spatial_edges.filter(
        (e: SpatialEdge) => e.predicate === "spatial_intersects",
      );
      expect(intersects.length).toBeGreaterThan(0);
      // spatial_clearance is always emitted for every pair
      const clearance = payload.spatial_edges.filter(
        (e: SpatialEdge) => e.predicate === "spatial_clearance",
      );
      expect(clearance.length).toBeGreaterThan(0);
    } finally {
      rmSync(outDir, { recursive: true, force: true });
    }
  });
});
