// Sprint RUST-MIG-1 Task 3 — scaffold crate (intentional red).
//
// Task 6 lands mahalanobis_distance (N4) here (conditional on
//   Task 1 hot verdict + no sklearn coupling on fit path).
// Task 7 lands sliced_wasserstein (N1) here.
//
// Both will use nalgebra (dense linalg, covariance invert) and
// ndarray (zero-copy numpy bridge via numpy 0.22 when pyo3_shim
// re-exports us in Tasks 6/7).

#[cfg(test)]
mod tests {
    #[test]
    fn mahalanobis_module_exists() {
        // intentional red — will go green in Task 6
        panic!("mahalanobis module not yet implemented");
    }
}
