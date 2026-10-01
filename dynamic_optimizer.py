"""
Dynamic Optimization Manager for IPL
Based on research: "Intelligent Compilers" (Cavazos et al.)
and dynamic optimization methodologies

This module implements:
- Runtime profiling and hot path detection
- JIT compilation for frequently executed code
- Adaptive optimization based on runtime behavior
- Feedback-directed optimization
- Performance monitoring and tuning
"""

import time
import threading
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import hashlib
import pickle


class OptimizationLevel(Enum):
    """Optimization levels for JIT compilation"""
    NONE = 0
    BASIC = 1  # Simple inlining, constant folding
    INTERMEDIATE = 2  # Loop unrolling, common subexpression elimination
    AGGRESSIVE = 3  # Full optimization with profile-guided feedback


class ExecutionMode(Enum):
    """Execution modes"""
    INTERPRETED = "interpreted"
    JIT_COMPILED = "jit_compiled"
    HYBRID = "hybrid"


@dataclass
class HotPath:
    """Represents a frequently executed code path"""
    function_name: str
    node_id: int
    execution_count: int
    total_time_ms: float
    avg_time_ms: float
    last_execution: float
    optimization_level: OptimizationLevel = OptimizationLevel.NONE
    compiled_code: Optional[bytes] = None


@dataclass
class ProfilingData:
    """Profiling data for a function or code block"""
    function_name: str
    node_id: int
    execution_count: int
    total_time_ms: float
    min_time_ms: float
    max_time_ms: float
    last_execution_time: float
    cache_hits: int = 0
    cache_misses: int = 0


@dataclass
class OptimizationDecision:
    """Decision about whether to optimize a code path"""
    should_optimize: bool
    optimization_level: OptimizationLevel
    reason: str
    confidence: float


class DynamicOptimizer:
    """
    Dynamic optimization manager for IPL runtime.

    Implements runtime profiling, hot path detection, and JIT compilation
    as described in Cavazos et al.'s work on dynamic optimization.
    """

    def __init__(self,
                 hot_path_threshold: int = 100,
                 time_threshold_ms: float = 1.0,
                 max_hot_paths: int = 50,
                 enable_jit: bool = True):
        """
        Initialize dynamic optimizer.

        Args:
            hot_path_threshold: Minimum executions to consider a hot path
            time_threshold_ms: Minimum execution time to consider optimization
            max_hot_paths: Maximum number of hot paths to track
            enable_jit: Enable JIT compilation
        """
        self.hot_path_threshold = hot_path_threshold
        self.time_threshold_ms = time_threshold_ms
        self.max_hot_paths = max_hot_paths
        self.enable_jit = enable_jit

        # Profiling data
        self.profiling_data: Dict[int, ProfilingData] = {}
        self.hot_paths: Dict[int, HotPath] = {}
        self.execution_mode = ExecutionMode.INTERPRETED

        # Compilation cache
        self.compilation_cache: Dict[int, bytes] = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0
        }

        # Optimization history
        self.optimization_history: List[Dict[str, Any]] = []

        # Thread safety
        self.lock = threading.RLock()

        # Optimization callbacks
        self.optimization_callbacks: List[Callable] = []

    def register_optimization_callback(self, callback: Callable):
        """Register callback for optimization events"""
        self.optimization_callbacks.append(callback)

    def record_execution(self,
                        node_id: int,
                        function_name: str,
                        execution_time_ms: float,
                        success: bool = True):
        """
        Record execution of a code node for profiling.

        Args:
            node_id: AST node ID
            function_name: Name of function being executed
            execution_time_ms: Execution time in milliseconds
            success: Whether execution succeeded
        """
        with self.lock:
            # Get or create profiling data
            if node_id not in self.profiling_data:
                self.profiling_data[node_id] = ProfilingData(
                    function_name=function_name,
                    node_id=node_id,
                    execution_count=0,
                    total_time_ms=0.0,
                    min_time_ms=float('inf'),
                    max_time_ms=0.0,
                    last_execution_time=0.0
                )

            # Update profiling data
            data = self.profiling_data[node_id]
            data.execution_count += 1
            data.total_time_ms += execution_time_ms
            data.min_time_ms = min(data.min_time_ms, execution_time_ms)
            data.max_time_ms = max(data.max_time_ms, execution_time_ms)
            data.last_execution_time = execution_time_ms

            # Check if this is a hot path
            self._check_hot_path(node_id, data)

    def _check_hot_path(self, node_id: int, data: ProfilingData):
        """Check if code path should be considered hot and optimized"""
        if data.execution_count >= self.hot_path_threshold:
            avg_time = data.total_time_ms / data.execution_count

            if avg_time >= self.time_threshold_ms:
                # This is a hot path
                if node_id not in self.hot_paths:
                    hot_path = HotPath(
                        function_name=data.function_name,
                        node_id=node_id,
                        execution_count=data.execution_count,
                        total_time_ms=data.total_time_ms,
                        avg_time_ms=avg_time,
                        last_execution=time.time()
                    )
                    self.hot_paths[node_id] = hot_path

                    # Limit number of hot paths
                    if len(self.hot_paths) > self.max_hot_paths:
                        # Remove least frequently executed
                        sorted_paths = sorted(
                            self.hot_paths.values(),
                            key=lambda x: x.execution_count
                        )
                        oldest = sorted_paths[0]
                        del self.hot_paths[oldest.node_id]

                    # Trigger optimization decision
                    decision = self._make_optimization_decision(hot_path)
                    if decision.should_optimize:
                        self._optimize_hot_path(hot_path, decision)

    def _make_optimization_decision(self, hot_path: HotPath) -> OptimizationDecision:
        """
        Make decision about whether to optimize a hot path.

        Uses heuristic based on execution frequency and time,
        as described in Cavazos et al.'s work.
        """
        # Simple heuristic: higher frequency and time = more aggressive optimization
        if hot_path.execution_count > self.hot_path_threshold * 10:
            return OptimizationDecision(
                should_optimize=True,
                optimization_level=OptimizationLevel.AGGRESSIVE,
                reason=f"Very hot path: {hot_path.execution_count} executions",
                confidence=0.9
            )
        elif hot_path.execution_count > self.hot_path_threshold * 5:
            return OptimizationDecision(
                should_optimize=True,
                optimization_level=OptimizationLevel.INTERMEDIATE,
                reason=f"Hot path: {hot_path.execution_count} executions",
                confidence=0.8
            )
        elif hot_path.execution_count > self.hot_path_threshold:
            return OptimizationDecision(
                should_optimize=True,
                optimization_level=OptimizationLevel.BASIC,
                reason=f"Warm path: {hot_path.execution_count} executions",
                confidence=0.7
            )
        else:
            return OptimizationDecision(
                should_optimize=False,
                optimization_level=OptimizationLevel.NONE,
                reason="Not hot enough for optimization",
                confidence=0.5
            )

    def _optimize_hot_path(self, hot_path: HotPath, decision: OptimizationDecision):
        """
        Optimize a hot path using JIT compilation.

        Args:
            hot_path: Hot path to optimize
            decision: Optimization decision
        """
        if not self.enable_jit:
            return

        # Check if already compiled
        if hot_path.node_id in self.compilation_cache:
            self.cache_stats['hits'] += 1
            return

        self.cache_stats['misses'] += 1

        # In a real implementation, this would:
        # 1. Extract the code for the hot path
        # 2. Apply optimizations based on optimization level
        # 3. Compile to bytecode or machine code
        # 4. Cache the compiled code

        # For now, simulate compilation
        compiled_code = self._simulate_compilation(hot_path, decision.optimization_level)
        self.compilation_cache[hot_path.node_id] = compiled_code
        hot_path.compiled_code = compiled_code
        hot_path.optimization_level = decision.optimization_level

        # Record optimization
        self.optimization_history.append({
            'timestamp': time.time(),
            'node_id': hot_path.node_id,
            'function_name': hot_path.function_name,
            'optimization_level': decision.optimization_level.value,
            'reason': decision.reason,
            'confidence': decision.confidence
        })

        # Notify callbacks
        for callback in self.optimization_callbacks:
            callback(hot_path, decision)

    def _simulate_compilation(self, hot_path: HotPath, level: OptimizationLevel) -> bytes:
        """
        Simulate JIT compilation (placeholder for real implementation).

        In a real implementation, this would:
        - Parse the AST for the hot path
        - Apply optimization passes based on level
        - Generate optimized bytecode or machine code
        """
        # Simulate compilation by hashing the hot path info
        compilation_data = {
            'node_id': hot_path.node_id,
            'function_name': hot_path.function_name,
            'optimization_level': level.value,
            'timestamp': time.time()
        }
        return pickle.dumps(compilation_data)

    def get_compiled_code(self, node_id: int) -> Optional[bytes]:
        """Get compiled code for a node if available"""
        with self.lock:
            return self.compilation_cache.get(node_id)

    def get_profiling_statistics(self) -> Dict[str, Any]:
        """Get profiling statistics"""
        with self.lock:
            total_executions = sum(d.execution_count for d in self.profiling_data.values())
            total_time = sum(d.total_time_ms for d in self.profiling_data.values())

            return {
                'total_nodes_profiled': len(self.profiling_data),
                'total_executions': total_executions,
                'total_time_ms': total_time,
                'avg_time_per_execution': total_time / max(1, total_executions),
                'hot_paths_count': len(self.hot_paths),
                'cache_hits': self.cache_stats['hits'],
                'cache_misses': self.cache_stats['misses'],
                'cache_hit_rate': self.cache_stats['hits'] / max(1,
                    self.cache_stats['hits'] + self.cache_stats['misses']),
                'optimizations_performed': len(self.optimization_history)
            }

    def get_hot_paths(self, limit: int = 10) -> List[HotPath]:
        """Get top hot paths by execution count"""
        with self.lock:
            sorted_paths = sorted(
                self.hot_paths.values(),
                key=lambda x: x.execution_count,
                reverse=True
            )
            return sorted_paths[:limit]

    def get_profiling_data(self, node_id: int) -> Optional[ProfilingData]:
        """Get profiling data for a specific node"""
        with self.lock:
            return self.profiling_data.get(node_id)

    def reset_profiling(self):
        """Reset all profiling data"""
        with self.lock:
            self.profiling_data.clear()
            self.hot_paths.clear()
            self.compilation_cache.clear()
            self.cache_stats = {'hits': 0, 'misses': 0}
            self.optimization_history.clear()

    def export_profiling_data(self) -> Dict[str, Any]:
        """Export profiling data for analysis"""
        with self.lock:
            return {
                'profiling_data': {
                    node_id: {
                        'function_name': data.function_name,
                        'execution_count': data.execution_count,
                        'total_time_ms': data.total_time_ms,
                        'avg_time_ms': data.total_time_ms / max(1, data.execution_count),
                        'min_time_ms': data.min_time_ms,
                        'max_time_ms': data.max_time_ms,
                        'cache_hits': data.cache_hits,
                        'cache_misses': data.cache_misses
                    }
                    for node_id, data in self.profiling_data.items()
                },
                'hot_paths': {
                    node_id: {
                        'function_name': path.function_name,
                        'execution_count': path.execution_count,
                        'avg_time_ms': path.avg_time_ms,
                        'optimization_level': path.optimization_level.value,
                        'is_compiled': path.compiled_code is not None
                    }
                    for node_id, path in self.hot_paths.items()
                },
                'statistics': self.get_profiling_statistics(),
                'optimization_history': self.optimization_history
            }


class FeedbackOptimizer:
    """
    Feedback-directed optimizer that uses runtime feedback
    to guide optimization decisions.

    Based on Cavazos et al.'s work on feedback-directed optimization.
    """

    def __init__(self, window_size: int = 100):
        """
        Initialize feedback optimizer.

        Args:
            window_size: Size of sliding window for feedback analysis
        """
        self.window_size = window_size
        self.feedback_history: deque = deque(maxlen=window_size)
        self.performance_baseline: Optional[float] = None

    def record_feedback(self,
                       node_id: int,
                       optimization_level: OptimizationLevel,
                       performance_gain: float):
        """
        Record feedback about optimization effectiveness.

        Args:
            node_id: AST node ID
            optimization_level: Optimization level applied
            performance_gain: Performance improvement (speedup factor)
        """
        self.feedback_history.append({
            'node_id': node_id,
            'optimization_level': optimization_level.value,
            'performance_gain': performance_gain,
            'timestamp': time.time()
        })

    def analyze_feedback(self) -> Dict[str, Any]:
        """Analyze feedback history to guide future optimizations"""
        if not self.feedback_history:
            return {'status': 'insufficient_data'}

        # Calculate average performance gain by optimization level
        gains_by_level = defaultdict(list)
        for feedback in self.feedback_history:
            level = feedback['optimization_level']
            gain = feedback['performance_gain']
            gains_by_level[level].append(gain)

        avg_gains = {
            level: sum(gains) / len(gains)
            for level, gains in gains_by_level.items()
        }

        # Find most effective optimization level
        best_level = max(avg_gains.items(), key=lambda x: x[1]) if avg_gains else (None, 0)

        return {
            'status': 'analyzed',
            'total_feedback_points': len(self.feedback_history),
            'average_gains_by_level': avg_gains,
            'best_optimization_level': best_level[0],
            'best_average_gain': best_level[1]
        }

    def get_optimization_recommendation(self,
                                        node_id: int,
                                        execution_frequency: int) -> OptimizationLevel:
        """
        Get optimization recommendation based on feedback.

        Args:
            node_id: AST node ID
            execution_frequency: How often the code is executed

        Returns:
            Recommended optimization level
        """
        analysis = self.analyze_feedback()

        if analysis['status'] == 'insufficient_data':
            # Default to conservative optimization
            if execution_frequency > 1000:
                return OptimizationLevel.AGGRESSIVE
            elif execution_frequency > 100:
                return OptimizationLevel.INTERMEDIATE
            else:
                return OptimizationLevel.BASIC

        # Use feedback to guide decision
        best_level = analysis['best_optimization_level']
        if best_level is not None:
            return OptimizationLevel(best_level)

        # Fallback to frequency-based decision
        if execution_frequency > 1000:
            return OptimizationLevel.AGGRESSIVE
        elif execution_frequency > 100:
            return OptimizationLevel.INTERMEDIATE
        else:
            return OptimizationLevel.BASIC


# Test the dynamic optimizer
if __name__ == "__main__":
    print("Testing Dynamic Optimizer")

    # Initialize optimizer
    optimizer = DynamicOptimizer(
        hot_path_threshold=10,
        time_threshold_ms=0.5,
        enable_jit=True
    )

    # Simulate executions
    for i in range(150):
        node_id = 1
        function_name = "test_function"
        execution_time = 2.0 + (i % 10) * 0.1  # Varying execution times
        optimizer.record_execution(node_id, function_name, execution_time)

    # Get statistics
    stats = optimizer.get_profiling_statistics()
    print("\nProfiling Statistics:")
    print(json.dumps(stats, indent=2))

    # Get hot paths
    hot_paths = optimizer.get_hot_paths(limit=5)
    print("\nHot Paths:")
    for path in hot_paths:
        print(f"  {path.function_name}: {path.execution_count} executions, "
              f"{path.avg_time_ms:.2f}ms avg, level={path.optimization_level.value}")

    # Export profiling data
    export_data = optimizer.export_profiling_data()
    print(f"\nExported profiling data with {len(export_data['profiling_data'])} nodes")

    print("\nDynamic Optimizer test completed!")
