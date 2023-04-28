"""
Usage:
```bash
opentelemetry-instrument --traces_exporter console \
    --metrics_exporter console \
    python example_use_loguru_opentelemetry_sink.py
```

"""


from loguru_opentelemetry_sink import get_ot_logger

if __name__ == "__main__":
    logger = get_ot_logger()

    def greet(name):
        logger.info(f"Hello {name}")
        return f"Hello {name}"

    greet("Joseph")
