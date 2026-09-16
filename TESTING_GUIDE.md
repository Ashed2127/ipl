# How to Run and Test the Hierarchical AI Engine Intelligence

## Quick Start

### 1. Run the Comprehensive Test Suite
```bash
python3 test_hierarchical_ai.py
```

This tests all AI engine components:
- Basic AI engine functionality
- Token optimization system
- Intelligent caching system
- Speculative execution pipeline
- IPL compiler integration
- Fallback mechanisms

### 2. Test with Real IPL Examples

#### Hierarchical AI Mode (Default)
```bash
python3 cli.py run examples/01_intelligent_variables.ipl
python3 cli.py audit examples/08_neuro_symbolic_compiler.ipl
```

#### Traditional Mode (No AI)
```bash
python3 cli.py run examples/01_intelligent_variables.ipl --traditional
python3 cli.py audit examples/08_neuro_symbolic_compiler.ipl --traditional
```

### 3. Test Custom AI Integration Files

#### Basic AI Integration Test
```bash
python3 cli.py audit test_ai_integration.ipl
```

#### Advanced Intelligence Test
```bash
python3 cli.py audit test_ai_intelligence.ipl
```

## Understanding the AI Engine Statistics

When you run with `audit` mode, you'll see detailed AI engine statistics:

### AI Engine Overview
- **Total Requests**: Number of AI calls made during execution
- **Tier Usage**: Distribution across the 3 model tiers

### Model Tier Usage
- **tier_1_lightning**: Fast pattern matching (<1ms) - handles simple tasks
- **tier_2_specialized**: Semantic analysis (10-50ms) - handles moderate tasks  
- **tier_3_reasoning**: Deep reasoning (100-500ms) - handles complex tasks

### Token Usage & Cost
- **Total Tokens**: Combined input/output tokens across all AI calls
- **Total Cost**: Estimated cost based on tier-specific pricing
- **Avg Tokens/Request**: Efficiency metric for token usage

### Cache Performance
- **Cache Hit Rate**: Percentage of requests served from cache
- **Cache Size**: Current cache usage vs maximum capacity
- **Hits/Misses**: Absolute counts for cache performance

## Interactive Testing

### Start IPL REPL with Hierarchical AI
```bash
python3 cli.py repl
```

### Test Commands in REPL
```ipl
// Test intent processing with AI
let age: Int = intent "extract user_age 25 from document" as Int
print age
print taint_of(age)

// View AI engine statistics
print ai_stats()

// Test currency extraction
let cost: Currency = intent "price is 100 dollars" as Currency
print cost

// Test sentiment analysis
let feedback: Sentiment = intent "the service was fantastic" as Sentiment
print feedback
```

### Start REPL with Traditional Mode
```bash
python3 cli.py repl --traditional
```

## Performance Testing

### Run Performance Comparison
```bash
python3 performance_comparison.py
```

This compares:
- Execution time between hierarchical AI and traditional modes
- Success rates for both modes
- Performance ratios and improvements

## Intelligence Testing Scenarios

### 1. Type Inference Intelligence
**Test**: Converting natural language to specific types
```ipl
let age: Int = intent "the user age is twenty-five" as Int
let price: Currency = intent "cost is ninety-nine dollars" as Currency
let date: Date = intent "meeting is tomorrow at 3pm" as Date
```

### 2. Semantic Understanding
**Test**: Extracting meaning from context
```ipl
let budget: Currency = intent "allocate 12500 euros for Q3 project" as Currency
let quantity: Quantity = intent "latency is 450 milliseconds" as Quantity
```

### 3. Sentiment Analysis
**Test**: Determining emotional tone
```ipl
let positive: Sentiment = intent "absolutely fantastic service" as Sentiment
let negative: Sentiment = intent "horrible experience, crashed repeatedly" as Sentiment
```

### 4. Complex Intent Processing
**Test**: Multi-part instructions
```ipl
let complex: Currency = intent "allocate budget of 12500 euros for the third quarter project with additional contingency" as Currency
```

### 5. Error Correction
**Test**: Self-healing capabilities
```ipl
let user_age: Int = intent "extract user_age twenty-five from document" as Int
// AI should correct "twenty-five" to 25
```

## Advanced Testing

### Test Caching Behavior
Run the same script multiple times to see cache hit rate improve:
```bash
# First run - cache misses
python3 cli.py audit test_ai_integration.ipl

# Second run - should see cache hits
python3 cli.py audit test_ai_integration.ipl

# Third run - cache hit rate should be higher
python3 cli.py audit test_ai_integration.ipl
```

### Test Token Optimization
Examine token usage statistics to see optimization effectiveness:
```bash
python3 cli.py audit test_ai_intelligence.ipl
```

Look for:
- Average tokens per request (lower is better)
- Total cost (should be minimal for Tier 1)
- Tier distribution (should favor Tier 1 for simple tasks)

### Test Fallback Mechanisms
Test what happens when AI fails:
```bash
python3 cli.py run test_ai_integration.ipl --traditional
```

Compare results to ensure fallback works correctly.

## Monitoring and Debugging

### Enable Detailed Logging
The AI engine provides detailed statistics through the `ai_stats()` function:

```ipl
print ai_stats()
```

This returns:
```json
{
  "total_requests": 2,
  "tier_usage": {
    "tier_1_lightning": 2,
    "tier_2_specialized": 0,
    "tier_3_reasoning": 0
  },
  "token_statistics": {
    "total_tokens_used": 34,
    "total_cost_usd": 0.0,
    "average_tokens_per_request": 17.0
  },
  "cache_statistics": {
    "cache_hit_rate": 0.0,
    "cache_size": 2,
    "hit_count": 0,
    "miss_count": 2
  }
}
```

### Analyze Audit Trails
Use audit mode to see the complete compilation process:
```bash
python3 cli.py audit examples/08_neuro_symbolic_compiler.ipl
```

Look for:
- INTENT_INGESTION phases
- SYSTEM1_NEURAL_PARSE phases
- SELF_CORRECTION_CYCLE phases
- AI engine statistics at the end

## Expected Results

### Hierarchical AI Mode
- **Speed**: Comparable or faster than traditional for most tasks
- **Intelligence**: Better semantic understanding and type inference
- **Token Efficiency**: Optimized token usage with intelligent caching
- **Cost**: Minimal cost due to Tier 1 dominance for simple tasks

### Traditional Mode
- **Speed**: Consistent performance without AI overhead
- **Intelligence**: Rule-based processing with existing semantic engine
- **Reliability**: Proven fallback mechanism
- **Compatibility**: Full backward compatibility

## Troubleshooting

### AI Engine Not Working
1. Check if hierarchical AI is disabled: `--traditional` flag
2. Verify imports in `hierarchical_ai_engine.py`
3. Check for errors in test output
4. Ensure fallback mechanisms work

### Poor Cache Performance
1. Run scripts multiple times to build cache
2. Check cache size limits (default: 1000 entries)
3. Verify TTL settings (default: 3600 seconds)
4. Monitor hit rate improvement over time

### High Token Usage
1. Check if complex tasks are triggering Tier 3
2. Review prompt optimization effectiveness
3. Consider task complexity classification
4. Monitor tier distribution in statistics

## Next Steps

### Production Deployment
1. Monitor AI engine statistics in production
2. Set up cost tracking and budgeting
3. Configure cache parameters for your workload
4. Implement monitoring for tier distribution

### Model Integration
1. Replace simulated models with real AI models
2. Configure GPU acceleration for Tier 2/3
3. Fine-tune models on IPL-specific datasets
4. Implement model versioning and A/B testing

### Performance Optimization
1. Tune cache size and TTL for your patterns
2. Adjust complexity classification thresholds
3. Optimize token limits and costs
4. Implement distributed caching for scale

## Conclusion

The hierarchical AI engine provides a sophisticated balance of intelligence and speed. By following this testing guide, you can:

- **Verify Intelligence**: Test semantic understanding, type inference, and sentiment analysis
- **Measure Performance**: Compare AI vs traditional modes
- **Monitor Efficiency**: Track token usage, costs, and cache performance
- **Ensure Reliability**: Test fallback mechanisms and error handling
- **Optimize Production**: Tune parameters for your specific workload

The system is designed to be production-ready with comprehensive monitoring, graceful degradation, and continuous optimization capabilities.