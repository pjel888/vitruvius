import type { Resource, SourceFamily } from './types';

export function authorityScoreFromTier(tier?: number) {
  switch (tier) {
    case 1: return 0.95;
    case 2: return 0.82;
    case 3: return 0.72;
    case 4: return 0.6;
    case 5: return 0.35;
    default: return 0.2;
  }
}

export function sourceFamilyMap(families: SourceFamily[]) {
  return new Map(families.map((family) => [family.id, family]));
}

export function approvedSourceFamilyIds(families: SourceFamily[]) {
  return new Set(families.map((family) => family.id));
}

export function authorityScoreForResource(resource: Resource, families: SourceFamily[]) {
  const familyById = sourceFamilyMap(families);
  const familyScores = (resource.sourceFamilyIds || [])
    .map((id) => familyById.get(id))
    .filter((family): family is SourceFamily => Boolean(family))
    .map((family) => authorityScoreFromTier(family.authorityTier));
  if (familyScores.length > 0) return Math.max(...familyScores);
  return authorityScoreFromTier(resource.authorityTier);
}

export function sourceFamilyMatchesUrl(resource: Resource, family: SourceFamily) {
  const url = resource.canonicalUrl || resource.url || resource.landingPageUrl || resource.pdfUrl || '';
  if (!url || !family.domains?.length) return false;
  try {
    const host = new URL(url).hostname.replace(/^www\./, '').toLowerCase();
    return family.domains.some((domain) => host === domain || host.endsWith(`.${domain}`));
  } catch {
    return false;
  }
}
