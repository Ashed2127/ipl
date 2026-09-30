# IPL Consolidation Log - Phase 0

## Date: 2026-09-30

## Overview
This document records the consolidation of the IPL codebase to a single canonical compiler pipeline, removing duplicate components and unsound AI-based security decisions.

## Files Deleted

### Compiler Overlap (2 files)
- `neural_compiler.py` - Duplicate orchestration layer using intelligent_* components
- `unified_neural_compiler.py` - Duplicate orchestration layer using real_neural_* components

### Intelligent Suite (7 files)
- `intelligent_lexer.py` - Duplicate lexer with "neural" pattern matching
- `intelligent_parser.py` - Duplicate parser with AI-enhanced parsing
- `intelligent_semantic_analyzer.py` - Duplicate semantic analyzer
- `intelligent_type_system.py` - Duplicate type system
- `intelligent_security_analyzer.py` - Duplicate security analyzer
- `intelligent_optimizer.py` - Duplicate optimizer
- `intelligent_code_generator.py` - Duplicate code generator

### Real Neural Suite (10 files)
- `real_neural_lexer.py` - Third lexer implementation
- `real_neural_lexer_v2.py` - Fourth lexer implementation
- `real_neural_parser.py` - Third parser implementation
- `real_neural_parser_fast.py` - Fourth parser implementation
- `real_neural_parser_truly_neural.py` - Fifth parser implementation
- `real_neural_semantic_analyzer.py` - Third semantic analyzer
- `real_neural_type_system.py` - Third type system
- `real_neural_security_analyzer.py` - Third security analyzer
- `real_neural_optimizer.py` - Third optimizer
- `real_neural_code_generator.py` - Third code generator

### AI/Expert Components (10 files)
- `hierarchical_ai_engine.py` - 3-tier speculative AI with LLM calls. Uses confidence scores for security decisions. **REASON**: Unsound for security - AI confidence should not be the final gate.
- `expert_system.py` - Pattern matching with pre-written "reasoning" strings. **REASON**: No actual symbolic verification, just hardcoded patterns.
- `expert_reasoning_engine.py` - Adds chain-of-thought strings to expert_system. **REASON**: No actual symbolic reasoning.
- `ai_expert_system.py` - Wrapper around expert_system. **REASON**: Duplicate functionality.
- `ai_decision_analyzer.py` - Tracks AI decision statistics. **REASON**: No longer needed without AI components.
- `ai_first_config.py` - AI-first mode configuration. **REASON**: AI-first mode removed as unsound.
- `ai_request_controller.py` - AI-based request controller. **REASON**: AI-based security decisions unsound.
- `simulated_ai_controller.py` - Simulated AI controller. **REASON**: Test file for removed components.
- `simple_pattern_controller.py` - Pattern-based controller. **REASON**: Test file for removed components.
- `enhanced_neural_security_analyzer.py` - Enhanced neural security analyzer. **REASON**: Uses "neural" patterns without verification.

### Authorization System (1 file)
- `authorization_system.py` - Hand-written Python that never routes through runtime.py's taint pipeline. **REASON**: Bypasses the core security mechanism. Will be replaced with an IPL program that actually uses taint tracking.

### Brute Force/Controller Files (7 files - to be consolidated)
- `brute_force_ai_controller.py` - Will be merged into consolidated test
- `brute_force_test_ai.py` - Will be merged into consolidated test
- `brute_force_test.py` - Will be merged into consolidated test
- `ipl_brute_force_attack_detection.py` - Will be merged into consolidated test
- `ipl_brute_force_fast.py` - Will be merged into consolidated test
- `ipl_brute_force_self_control.py` - Will be merged into consolidated test
- `simple_brute_force_test.py` - Will be merged into consolidated test

## Canonical Pipeline (Retained)

### Core Components
- `taint.py` - Sound taint lattice (UNTRUSTED < SANITIZED < TRUSTED) with correct combine() semantics. **STATUS**: Architecturally correct, unchanged.
- `lexer.py` - Deterministic lexer for IPL. **STATUS**: Retained as canonical lexer.
- `parser.py` - Deterministic parser for IPL. **STATUS**: Retained as canonical parser.
- `semantic_engine.py` - Pattern-based semantic extraction. **STATUS**: Retained for natural language processing.
- `security_engine.py` - Contains sanitize_string() (currently sink-agnostic). **STATUS**: Will be fixed in Phase 1.
- `ast_nodes.py` - AST node definitions. **STATUS**: Retained.
- `tokens.py` - Token definitions. **STATUS**: Retained.
- `formatter.py` - Code formatting. **STATUS**: Retained.
- `compiler.py` - Main compiler. **STATUS**: Updated to remove AI/expert/authorization dependencies.
- `runtime.py` - Runtime interpreter. **STATUS**: Updated to remove authorization dependencies.
- `cli.py` - Command-line interface. **STATUS**: Partially updated, needs more cleanup.

### Changes to Canonical Files

#### compiler.py
- Removed imports: hierarchical_ai_engine, authorization_system, ai_first_config, expert_system, expert_reasoning_engine
- Simplified LocalInferenceRuntime: Removed hierarchical AI, authorization, AI-first mode
- Simplified NeuroSymbolicCompiler: Removed expert system, authorization system
- Kept: MathematicalFirewall, VerifiedAuditTrace, SemanticEngine integration
- Kept: taint tracking via TaintTag and TaintLevel

#### runtime.py
- Removed: use_hierarchical_ai, enable_authorization, tier3_model parameters
- Removed: authorization system integration
- Kept: taint tracking, sink enforcement (db_write, file_write)

#### cli.py
- Removed: authorization_system import
- Removed: _print_auth_stats function
- Removed: manage_users function
- Partially updated: run_file function (needs more cleanup)
- Updated: banner text to reflect simplified architecture

## Files to Create

### test_adversarial_attacks.py
Will consolidate the strongest logic from all brute force files:
- Repetitive pattern detection from ipl_brute_force_attack_detection.py
- Attack patterns (credential stuffing, password spray, rapid fire) from brute_force_test_ai.py
- Multi-threaded and sustained load tests from simple_brute_force_test.py

### examples/authorization_demo.ipl
Will replace authorization_system.py with an actual IPL program that:
- Uses taint tracking
- Demonstrates sanitize_string usage
- Shows db_write sink enforcement
- Demonstrates the full security pipeline

### CONSOLIDATION_LOG.md
This file - documents the consolidation process.

## Rationale for Deletions

### Why AI Components Were Deleted
The brief states: "Any component that uses an LLM or 'neural' classifier to make a compile-blocking security decision is being used unsoundly. AI may only PROPOSE (a parse, a candidate sanitizer, a candidate invariant). A symbolic/solver-based check must VERIFY before anything is trusted. Never let a model's confidence score be the final gate."

All deleted AI components used confidence scores or "neural" classifications as the final security decision, which violates this principle.

### Why Authorization System Was Deleted
The brief states: "authorization_system.py (the flagship security demo) is hand-written Python that never routes through runtime.py's taint pipeline, so it demonstrates nothing about IPL's actual guarantees."

The authorization system was external to the IPL language and didn't use the taint tracking system, making it an ineffective demonstration of IPL's security capabilities.

### Why Multiple Compiler Implementations Were Deleted
The brief states: "compiler.py, neural_compiler.py, and unified_neural_compiler.py are three parallel, overlapping compiler entry points. intelligent_*.py and real_neural_*.py (including _v2, _fast, _truly_neural variants) are a second and third reimplementation of lexer/parser/typer/security/codegen. None of this is to be extended — it is to be deleted or merged."

Keeping multiple overlapping implementations makes the codebase unmaintainable and confuses the actual security guarantees.

## Next Steps

1. Complete CLI cleanup (remove remaining authorization/AI references)
2. Create consolidated test_adversarial_attacks.py
3. Create examples/authorization_demo.ipl
4. Test canonical pipeline still works
5. Update README.md to remove marketing claims about "neural" and "AI-powered"
6. Update ARCHITECTURE.md to reflect simplified architecture
7. Delete remaining brute force/controller files after consolidation
8. Delete test files that depend on removed components

## Verification

Before proceeding to Phase 1, ensure:
- [ ] Canonical pipeline (compiler.py + taint.py + runtime.py + lexer.py + parser.py) works
- [ ] All imports to deleted files are removed
- [ ] test_adversarial_attacks.py exists and tests taint tracking
- [ ] examples/authorization_demo.ipl exists and uses taint pipeline
- [ ] CLI works without errors
- [ ] README.md updated to remove stale marketing claims
- [ ] ARCHITECTURE.md updated to reflect simplified architecture
