"""
This module contains a custom sink for loguru that sends logs to OpenTelemetry.
"""

from loguru import logger
from opentelemetry import trace


def get_ot_logger():
    """
    This method returns a logger with a function that sinks to OpenTelemetry.

    Todo: Allow for a lot more things to be injected so the user can configure
    the parameters send to open telemetry:
    * TracerProvider()
    * BatchSpanProcessor()
    * OLTPSpanExporter()

    So you can configure like this:
    from loguru import logger
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

    # Configure the OpenTelemetry Tracer
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    # Configure the OpenTelemetry exporter
    otlp_exporter = OTLPSpanExporter()
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    """
    tracer = trace.get_tracer(__name__)

    # Custom Loguru sink function
    def otel_sink(message):
        record = message.record

        # Start a new span
        with tracer.start_as_current_span(f"LogRecord: {record['level']}") as span:
            span.set_attribute("logger.name", record["name"])
            span.set_attribute("logger.message", record["message"])
            span.set_attribute("logger.level", record["level"].name)
            span.set_attribute("logger.file", record["file"].path)
            span.set_attribute("logger.line", record["line"])
            span.set_attribute("logger.function", record["function"])

    # Add the custom sink to Loguru
    logger.add(otel_sink, level="DEBUG")
    return logger


if __name__ == "__main__":
    logger = get_ot_logger()
    logger.debug("This is a debug message")
    logger.error("This is an error message")
