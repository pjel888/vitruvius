const VERIFIED_RESOURCE_STATUSES = new Set([
  'metadata_verified',
  'link_verified',
  'identifier_verified',
  'local_file_verified',
  'content_verified',
  'human_reviewed',
  'reviewer_verified_metadata',
]);

export function isPositiveResourceVerificationStatus(status?: string | null) {
  return Boolean(status && VERIFIED_RESOURCE_STATUSES.has(status));
}
