from __future__ import annotations

from enum import StrEnum


class V1MonitoringWANMetric(StrEnum):
    """Allowed WAN metric values for v1 monitoring path link queries."""

    LATENCY = "latency"
    JITTER = "jitter"
    RX_LOSS = "rx_loss"
    TX_LOSS = "tx_loss"
    RX_THROUGHPUT = "rx_throughput"
    TX_THROUGHPUT = "tx_throughput"
    RX_BYTES = "rx_bytes"
    TX_BYTES = "tx_bytes"
    RX_PACKETS = "rx_packets"
    TX_PACKETS = "tx_packets"
