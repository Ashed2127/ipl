"""
Statistics Collection Framework for Continual Learning
Based on research: "Intelligent Compilers" (Cavazos et al.)
and continual learning methodologies

This module implements:
- Compilation statistics collection
- Runtime performance tracking
- Security check effectiveness monitoring
- Model performance metrics
- Empirical testing framework
"""

import json
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import os


class StatisticType(Enum):
    """Types of statistics to collect"""
    COMPILATION_TIME = "compilation_time"
    EXECUTION_TIME = "execution_time"
    SECURITY_CHECK_RESULT = "security_check_result"
    OPTIMIZATION_EFFECTIVENESS = "optimization_effectiveness"
    TAINT_PROPAGATION = "taint_propagation"
    PATTERN_DETECTION = "pattern_detection"
    ERROR_RATE = "error_rate"
    PERFORMANCE_METRIC = "performance_metric"


@dataclass
class CompilationStatistic:
    """Statistic from a single compilation"""
    timestamp: str
    program_hash: str
    compilation_time_ms: float
    num_nodes: int
    num_edges: int
    security_violations: int
    static_safe_sites: int
    dynamic_sites: int
    taint_propagation_steps: int
    optimization_flags: List[str]
    success: bool
    error_message: Optional[str] = None


@dataclass
class ExecutionStatistic:
    """Statistic from program execution"""
    timestamp: str
    program_hash: str
    execution_time_ms: float
    memory_usage_mb: float
    security_blocks: int
    runtime_taint_checks: int
    hot_path_executions: int
    cache_hits: int
    cache_misses: int
    success: bool
    error_message: Optional[str] = None


@dataclass
class SecurityCheckStatistic:
    """Statistic from security checks"""
    timestamp: str
    program_hash: str
    check_type: str  # static, dynamic, gnn
    detected_vulnerabilities: List[str]
    false_positives: int
    false_negatives: int
    true_positives: int
    true_negatives: int
    confidence_score: float
    processing_time_ms: float


@dataclass
class ModelPerformanceStatistic:
    """Statistic from ML model performance"""
    timestamp: str
    model_name: str
    model_version: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_time_ms: float
    inference_time_ms: float
    dataset_size: int


class StatisticsCollector:
    """
    Collects and manages statistics for continual learning.

    Based on Cavazos et al.'s approach of empirical testing and
    automatic statistics collection for intelligent compilers.
    """

    def __init__(self, db_path: str = "ipl_statistics.db"):
        """
        Initialize statistics collector.

        Args:
            db_path: Path to SQLite database for statistics storage
        """
        self.db_path = db_path
        self.conn = None
        self._initialize_database()

    def _initialize_database(self):
        """Initialize SQLite database with required tables"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Compilation statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compilation_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                program_hash TEXT,
                compilation_time_ms REAL,
                num_nodes INTEGER,
                num_edges INTEGER,
                security_violations INTEGER,
                static_safe_sites INTEGER,
                dynamic_sites INTEGER,
                taint_propagation_steps INTEGER,
                optimization_flags TEXT,
                success BOOLEAN,
                error_message TEXT
            )
        """)

        # Execution statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                program_hash TEXT,
                execution_time_ms REAL,
                memory_usage_mb REAL,
                security_blocks INTEGER,
                runtime_taint_checks INTEGER,
                hot_path_executions INTEGER,
                cache_hits INTEGER,
                cache_misses INTEGER,
                success BOOLEAN,
                error_message TEXT
            )
        """)

        # Security check statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_check_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                program_hash TEXT,
                check_type TEXT,
                detected_vulnerabilities TEXT,
                false_positives INTEGER,
                false_negatives INTEGER,
                true_positives INTEGER,
                true_negatives INTEGER,
                confidence_score REAL,
                processing_time_ms REAL
            )
        """)

        # Model performance statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_performance_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                model_name TEXT,
                model_version TEXT,
                accuracy REAL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                training_time_ms REAL,
                inference_time_ms REAL,
                dataset_size INTEGER
            )
        """)

        # Program variants table (for continual learning)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS program_variants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_hash TEXT,
                source_code TEXT,
                ast_hash TEXT,
                is_vulnerable BOOLEAN,
                vulnerability_type TEXT,
                first_seen TEXT,
                last_seen TEXT,
                execution_count INTEGER
            )
        """)

        self.conn.commit()

    def record_compilation(self, stat: CompilationStatistic):
        """Record compilation statistic"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO compilation_stats
            (timestamp, program_hash, compilation_time_ms, num_nodes, num_edges,
             security_violations, static_safe_sites, dynamic_sites,
             taint_propagation_steps, optimization_flags, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            stat.timestamp,
            stat.program_hash,
            stat.compilation_time_ms,
            stat.num_nodes,
            stat.num_edges,
            stat.security_violations,
            stat.static_safe_sites,
            stat.dynamic_sites,
            stat.taint_propagation_steps,
            json.dumps(stat.optimization_flags),
            stat.success,
            stat.error_message
        ))
        self.conn.commit()

    def record_execution(self, stat: ExecutionStatistic):
        """Record execution statistic"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO execution_stats
            (timestamp, program_hash, execution_time_ms, memory_usage_mb,
             security_blocks, runtime_taint_checks, hot_path_executions,
             cache_hits, cache_misses, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            stat.timestamp,
            stat.program_hash,
            stat.execution_time_ms,
            stat.memory_usage_mb,
            stat.security_blocks,
            stat.runtime_taint_checks,
            stat.hot_path_executions,
            stat.cache_hits,
            stat.cache_misses,
            stat.success,
            stat.error_message
        ))
        self.conn.commit()

    def record_security_check(self, stat: SecurityCheckStatistic):
        """Record security check statistic"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO security_check_stats
            (timestamp, program_hash, check_type, detected_vulnerabilities,
             false_positives, false_negatives, true_positives, true_negatives,
             confidence_score, processing_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            stat.timestamp,
            stat.program_hash,
            stat.check_type,
            json.dumps(stat.detected_vulnerabilities),
            stat.false_positives,
            stat.false_negatives,
            stat.true_positives,
            stat.true_negatives,
            stat.confidence_score,
            stat.processing_time_ms
        ))
        self.conn.commit()

    def record_model_performance(self, stat: ModelPerformanceStatistic):
        """Record model performance statistic"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO model_performance_stats
            (timestamp, model_name, model_version, accuracy, precision,
             recall, f1_score, training_time_ms, inference_time_ms, dataset_size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            stat.timestamp,
            stat.model_name,
            stat.model_version,
            stat.accuracy,
            stat.precision,
            stat.recall,
            stat.f1_score,
            stat.training_time_ms,
            stat.inference_time_ms,
            stat.dataset_size
        ))
        self.conn.commit()

    def record_program_variant(self,
                               program_hash: str,
                               source_code: str,
                               ast_hash: str,
                               is_vulnerable: bool,
                               vulnerability_type: Optional[str] = None):
        """Record program variant for continual learning"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        # Check if program already exists
        cursor.execute("""
            SELECT id, execution_count FROM program_variants
            WHERE program_hash = ?
        """, (program_hash,))

        result = cursor.fetchone()

        if result:
            # Update existing
            cursor.execute("""
                UPDATE program_variants
                SET last_seen = ?, execution_count = execution_count + 1
                WHERE id = ?
            """, (now, result[0]))
        else:
            # Insert new
            cursor.execute("""
                INSERT INTO program_variants
                (program_hash, source_code, ast_hash, is_vulnerable,
                 vulnerability_type, first_seen, last_seen, execution_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                program_hash,
                source_code,
                ast_hash,
                is_vulnerable,
                vulnerability_type,
                now,
                now
            ))

        self.conn.commit()

    def get_compilation_statistics(self,
                                   program_hash: Optional[str] = None,
                                   limit: int = 100) -> List[Dict[str, Any]]:
        """Get compilation statistics"""
        cursor = self.conn.cursor()

        if program_hash:
            cursor.execute("""
                SELECT * FROM compilation_stats
                WHERE program_hash = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (program_hash, limit))
        else:
            cursor.execute("""
                SELECT * FROM compilation_stats
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_execution_statistics(self,
                                 program_hash: Optional[str] = None,
                                 limit: int = 100) -> List[Dict[str, Any]]:
        """Get execution statistics"""
        cursor = self.conn.cursor()

        if program_hash:
            cursor.execute("""
                SELECT * FROM execution_stats
                WHERE program_hash = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (program_hash, limit))
        else:
            cursor.execute("""
                SELECT * FROM execution_stats
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_security_check_statistics(self,
                                     check_type: Optional[str] = None,
                                     limit: int = 100) -> List[Dict[str, Any]]:
        """Get security check statistics"""
        cursor = self.conn.cursor()

        if check_type:
            cursor.execute("""
                SELECT * FROM security_check_stats
                WHERE check_type = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (check_type, limit))
        else:
            cursor.execute("""
                SELECT * FROM security_check_stats
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_model_performance(self,
                             model_name: Optional[str] = None,
                             limit: int = 50) -> List[Dict[str, Any]]:
        """Get model performance statistics"""
        cursor = self.conn.cursor()

        if model_name:
            cursor.execute("""
                SELECT * FROM model_performance_stats
                WHERE model_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (model_name, limit))
        else:
            cursor.execute("""
                SELECT * FROM model_performance_stats
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_program_variants(self,
                            is_vulnerable: Optional[bool] = None,
                            limit: int = 100) -> List[Dict[str, Any]]:
        """Get program variants for continual learning"""
        cursor = self.conn.cursor()

        if is_vulnerable is not None:
            cursor.execute("""
                SELECT * FROM program_variants
                WHERE is_vulnerable = ?
                ORDER BY execution_count DESC
                LIMIT ?
            """, (is_vulnerable, limit))
        else:
            cursor.execute("""
                SELECT * FROM program_variants
                ORDER BY execution_count DESC
                LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def get_aggregated_statistics(self) -> Dict[str, Any]:
        """Get aggregated statistics for analysis"""
        cursor = self.conn.cursor()

        # Compilation stats
        cursor.execute("""
            SELECT
                COUNT(*) as total_compilations,
                AVG(compilation_time_ms) as avg_compilation_time,
                AVG(security_violations) as avg_violations,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_compilations
            FROM compilation_stats
        """)
        comp_stats = cursor.fetchone()

        # Execution stats
        cursor.execute("""
            SELECT
                COUNT(*) as total_executions,
                AVG(execution_time_ms) as avg_execution_time,
                AVG(memory_usage_mb) as avg_memory_usage,
                SUM(security_blocks) as total_security_blocks
            FROM execution_stats
        """)
        exec_stats = cursor.fetchone()

        # Security check stats
        cursor.execute("""
            SELECT
                check_type,
                COUNT(*) as total_checks,
                AVG(confidence_score) as avg_confidence,
                AVG(true_positives) as avg_true_positives,
                AVG(false_positives) as avg_false_positives
            FROM security_check_stats
            GROUP BY check_type
        """)
        security_stats = cursor.fetchall()
        security_columns = [desc[0] for desc in cursor.description]
        security_stats = [dict(zip(security_columns, row)) for row in security_stats]

        return {
            'compilation': {
                'total': comp_stats[0],
                'avg_time_ms': comp_stats[1],
                'avg_violations': comp_stats[2],
                'success_rate': comp_stats[3] / max(1, comp_stats[0])
            },
            'execution': {
                'total': exec_stats[0],
                'avg_time_ms': exec_stats[1],
                'avg_memory_mb': exec_stats[2],
                'total_blocks': exec_stats[3]
            },
            'security': security_stats
        }

    def export_statistics(self, output_path: str):
        """Export all statistics to JSON file"""
        stats = {
            'compilation': self.get_compilation_statistics(limit=1000),
            'execution': self.get_execution_statistics(limit=1000),
            'security_checks': self.get_security_check_statistics(limit=1000),
            'model_performance': self.get_model_performance(limit=100),
            'program_variants': self.get_program_variants(limit=1000),
            'aggregated': self.get_aggregated_statistics()
        }

        with open(output_path, 'w') as f:
            json.dump(stats, f, indent=2)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def compute_program_hash(source_code: str) -> str:
    """Compute hash of source code for deduplication"""
    return hashlib.sha256(source_code.encode()).hexdigest()


def compute_ast_hash(ast_node) -> str:
    """Compute hash of AST structure"""
    # Simple hash based on string representation
    # In production, use more sophisticated AST hashing
    return hashlib.sha256(str(ast_node).encode()).hexdigest()


# Test the statistics collector
if __name__ == "__main__":
    print("Testing Statistics Collector")

    # Initialize collector
    collector = StatisticsCollector(":memory:")  # Use in-memory database for testing

    # Record some test statistics
    comp_stat = CompilationStatistic(
        timestamp=datetime.now().isoformat(),
        program_hash="test_hash_1",
        compilation_time_ms=5.2,
        num_nodes=10,
        num_edges=15,
        security_violations=0,
        static_safe_sites=3,
        dynamic_sites=1,
        taint_propagation_steps=5,
        optimization_flags=["optimize", "inline"],
        success=True
    )
    collector.record_compilation(comp_stat)

    exec_stat = ExecutionStatistic(
        timestamp=datetime.now().isoformat(),
        program_hash="test_hash_1",
        execution_time_ms=2.1,
        memory_usage_mb=15.5,
        security_blocks=0,
        runtime_taint_checks=3,
        hot_path_executions=10,
        cache_hits=50,
        cache_misses=5,
        success=True
    )
    collector.record_execution(exec_stat)

    # Get statistics
    print("\nCompilation Statistics:")
    print(collector.get_compilation_statistics())

    print("\nExecution Statistics:")
    print(collector.get_execution_statistics())

    print("\nAggregated Statistics:")
    print(json.dumps(collector.get_aggregated_statistics(), indent=2))

    collector.close()
    print("\nStatistics Collector test completed!")
