/**
 * Type definitions for the Vitruvius Spatial Contract v1.0.0.
 *
 * These must stay byte-compatible with the Python validator at
 * `scripts/vitruvius/spatial/schema.py`. When the Python side
 * extends the schema, update this file in the same commit so
 * both sides of the cross-language contract advance atomically.
 */

/** Closed set of spatial relationship predicates. */
export type SpatialPredicate =
  | "spatial_intersects"
  | "spatial_clearance"
  | "spatial_adjacent_to"
  | "spatial_contains";

/** Supported length units for `SpatialEdge.value`. */
export type LengthUnit = "meters" | "millimeters" | "feet" | "inches";

/** Axis-aligned bounding box (world space). */
export interface BoundingBox {
  /** `[x, y, z]` of the minimum corner. */
  min: [number, number, number];
  /** `[x, y, z]` of the maximum corner. */
  max: [number, number, number];
}

/** A single spatial instance — e.g. a specific door in a building. */
export interface Instance {
  /** Unique ID starting with `"instance-"`. */
  instance_id: string;
  /** Mapped canonical concept ID starting with `"concept-"`. */
  canonical_concept_id: string;
  /** Optional AABB in world space. */
  bounding_box?: BoundingBox;
}

/** An edge describing a spatial relationship between two instances. */
export interface SpatialEdge {
  /** Source instance id (must start with `"instance-"`). */
  source_instance: string;
  /** Spatial predicate from the closed set. */
  predicate: SpatialPredicate;
  /** Target instance id (must start with `"instance-"`). */
  target_instance: string;
  /** Numeric value associated with the edge (e.g. clearance in meters). */
  value?: number;
  /** Unit for `value`. Ignored when `value` is absent. */
  unit?: LengthUnit;
}

/** Root contract for a single spatial context. */
export interface SpatialContract {
  /** Literal `"1.0.0"` — bumped via a coordinated cross-language change. */
  schema_version: "1.0.0";
  /** Context id starting with `"spatial-"` (stable per building / site). */
  spatial_context_id: string;
  /** ISO-8601 UTC timestamp. */
  generated_at_utc: string;
  /** Optional identifier for the daemon run that emitted this contract. */
  source_daemon?: string;
  /** Ordered list of spatial instances in this context. */
  instances: Instance[];
  /** Ordered list of spatial edges in this context. */
  spatial_edges: SpatialEdge[];
}
