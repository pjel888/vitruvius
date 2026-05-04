// Phase 6N — Resource-Only Promotion Apply Routes
// This file registers Express routes for:
// 1. POST /resources/review/external-candidates/:candidateId/promotion-apply-preview
// 2. POST /resources/review/external-candidates/:candidateId/promotion-apply
// 3. POST /resources/review/external-candidates/:candidateId/promotion-rollback-preview
// 4. POST /resources/review/external-candidates/:candidateId/promotion-rollback
//
// All routes require requireLocalDevAdmin.
// Only resource_only mode is supported.

import { Router, Request, Response } from 'express';
import { loadExternalCandidateRegistry } from './externalCandidateRegistry';
import { loadResourceLayerRegistry } from './registry';
import {
  buildResourceOnlyApplyPreview,
  applyResourceOnlyPromotion,
  buildRollbackPreview,
  applyRollback,
} from './externalCandidatePromotionApply';

const router = Router();

// ─── Middleware: requireLocalDevAdmin ─────────────────────────────────────

function requireLocalDevAdmin(req: Request, res: Response, next: Function): void {
  // In development, all requests are considered admin.
  // In production, this would check auth headers.
  next();
}

// ─── Route: Promotion Apply Preview ──────────────────────────────────────

router.post(
  '/resources/review/external-candidates/:candidateId/promotion-apply-preview',
  requireLocalDevAdmin,
  async (req: Request, res: Response) => {
    try {
      const { candidateId } = req.params;
      const { applyMode } = req.body;

      // Enforce resource_only mode
      if (applyMode && applyMode !== 'resource_only') {
        return res.status(400).json({
          success: false,
          gate: 'F0',
          message: 'Only resource_only mode is supported in Phase 6N',
          severity: 'stop',
          blockingGates: ['F0'],
        });
      }

      // Load candidate
      const repoRoot = process.cwd();
      const registry = loadExternalCandidateRegistry(repoRoot);
      const candidates = registry || [];
      const candidate = candidates.find((c: any) => (c.candidateId || c.id) === candidateId);

      if (!candidate) {
        return res.status(404).json({
          success: false,
          message: 'Candidate not found',
        });
      }

      // Build preview
      const preview = await buildResourceOnlyApplyPreview(candidate, [], {
        reviewer: req.body.reviewer,
        rationale: req.body.rationale,
        sourceOfContext: req.body.sourceOfContext,
        promotionCaveat: req.body.promotionCaveat,
      });

      return res.status(200).json({
        candidateId,
        applyMode: 'resource_only',
        gates: preview.gateResults.results.map(r => ({
          id: r.gate || '',
          label: getGateLabel(r.gate || ''),
          status: r.passed ? 'pass' : r.skipped ? 'skipped' : 'fail',
          message: r.message || '',
        })),
        allGatesPass: preview.canApply,
        blockingGates: preview.gateResults.blockingGates,
        resourceDraft: preview.resourceDraft,
        linkDrafts: [],
        caveats: preview.caveats,
        previewHash: preview.previewHash,
        canApply: preview.canApply,
      });
    } catch (err: any) {
      console.error('Promotion apply preview error:', err);
      return res.status(500).json({
        success: false,
        message: `Internal error: ${err.message}`,
      });
    }
  },
);

// ─── Route: Promotion Apply ──────────────────────────────────────────────

router.post(
  '/resources/review/external-candidates/:candidateId/promotion-apply',
  requireLocalDevAdmin,
  async (req: Request, res: Response) => {
    try {
      const { candidateId } = req.params;

      // Validate applyMode
      if (req.body.applyMode && req.body.applyMode !== 'resource_only') {
        return res.status(400).json({
          success: false,
          gate: 'F0',
          message: 'resource_and_links mode not implemented. Use applyMode: resource_only',
          severity: 'stop',
          blockingGates: ['F0'],
        });
      }

      // Validate required fields
      if (!req.body.reviewer || !req.body.rationale || !req.body.sourceOfContext) {
        return res.status(400).json({
          success: false,
          gate: 'I1',
          message: 'reviewer, rationale, and sourceOfContext are required',
          severity: 'stop',
          blockingGates: ['I1', 'I2', 'I3'],
        });
      }

      if (!req.body.previewHash) {
        return res.status(400).json({
          success: false,
          gate: 'H1',
          message: 'previewHash is required. Run promotion-apply-preview first.',
          severity: 'stop',
          blockingGates: ['H1'],
        });
      }

      // Build input
      const input = {
        candidateId,
        applyMode: 'resource_only' as const,
        reviewer: req.body.reviewer,
        rationale: req.body.rationale,
        sourceOfContext: req.body.sourceOfContext,
        previewHash: req.body.previewHash,
        acknowledgeWarnings: req.body.acknowledgeWarnings === true,
        promotionCaveat: req.body.promotionCaveat || req.body.rationale,
      };

      // Execute promotion
      const repoRoot = process.cwd();
      const result = await applyResourceOnlyPromotion(repoRoot, candidateId, input);

      if ('success' in result && !result.success) {
        return res.status(400).json(result);
      }

      return res.status(201).json(result);
    } catch (err: any) {
      console.error('Promotion apply error:', err);
      return res.status(500).json({
        success: false,
        message: `Internal error: ${err.message}`,
      });
    }
  },
);

// ─── Route: Rollback Preview ─────────────────────────────────────────────

router.post(
  '/resources/review/external-candidates/:candidateId/promotion-rollback-preview',
  requireLocalDevAdmin,
  async (req: Request, res: Response) => {
    try {
      const { candidateId } = req.params;
      const { resourceId } = req.body;

      if (!resourceId) {
        return res.status(400).json({
          success: false,
          message: 'resourceId is required',
        });
      }

      const repoRoot = process.cwd();
      const preview = await buildRollbackPreview(repoRoot, resourceId);

      if ('success' in preview && !preview.success) {
        return res.status(404).json(preview);
      }

      return res.status(200).json(preview);
    } catch (err: any) {
      console.error('Rollback preview error:', err);
      return res.status(500).json({
        success: false,
        message: `Internal error: ${err.message}`,
      });
    }
  },
);

// ─── Route: Rollback Apply ───────────────────────────────────────────────

router.post(
  '/resources/review/external-candidates/:candidateId/promotion-rollback',
  requireLocalDevAdmin,
  async (req: Request, res: Response) => {
    try {
      const { candidateId } = req.params;
      const { resourceId, reviewer, rationale, rollbackAction } = req.body;

      if (!resourceId) {
        return res.status(400).json({
          success: false,
          message: 'resourceId is required',
        });
      }
      if (!reviewer || !rationale) {
        return res.status(400).json({
          success: false,
          message: 'reviewer and rationale are required',
        });
      }
      if (!rollbackAction || !['hard_delete', 'mark_rolled_back'].includes(rollbackAction)) {
        return res.status(400).json({
          success: false,
          message: 'rollbackAction must be hard_delete or mark_rolled_back',
        });
      }

      const repoRoot = process.cwd();
      const result = await applyRollback(repoRoot, resourceId, {
        promotionDecisionId: '', // Will be looked up
        reviewer,
        rationale,
        rollbackAction: rollbackAction as 'hard_delete' | 'mark_rolled_back',
      });

      if ('success' in result && !result.success) {
        return res.status(400).json(result);
      }

      return res.status(200).json(result);
    } catch (err: any) {
      console.error('Rollback apply error:', err);
      return res.status(500).json({
        success: false,
        message: `Internal error: ${err.message}`,
      });
    }
  },
);

// ─── Helper: Gate Labels ─────────────────────────────────────────────────

function getGateLabel(gateId: string): string {
  const labels: Record<string, string> = {
    'A1': 'Candidate exists',
    'A2': 'Candidate ready for promotion review',
    'A3': 'Candidate not rejected',
    'A4': 'Candidate not deferred',
    'A5': 'Candidate not duplicate',
    'A6': 'Candidate not promotion blocked',
    'A7': 'Candidate has review history',
    'A8': 'Safety flags enabled',
    'B1': 'Title present',
    'B2': 'Resource type present',
    'B3': 'Source type present',
    'B4': 'No placeholder URL/DOI/ISBN',
    'B5': 'No fake metadata',
    'B7': 'No duplicate resource',
    'C4': 'No unsupported source verification',
    'C5': 'No unsupported existence claims',
    'D1': 'Rights status present',
    'D2': 'Rights status compatible',
    'E1': 'Standards context present',
    'E2': 'No placeholder standards context',
    'E3': 'ASCE 7 / ACI 318 not blocked',
    'E4': 'No unsupported governing claim',
    'F0': 'Mode supported',
    'G3': 'Learner visibility safe',
    'H1': 'Preview hash provided',
    'H3': 'Warnings acknowledged',
    'I1': 'Reviewer provided',
    'I2': 'Rationale provided',
    'I3': 'Source of context provided',
    'I6': 'Promotion caveat provided',
  };
  return labels[gateId] || `Gate ${gateId}`;
}

// ─── Route Registration Helper ────────────────────────────────────────────

function registerPromotionApplyRoutes(app: Router): void {
  app.use('/', router);
}

export { router, registerPromotionApplyRoutes };
