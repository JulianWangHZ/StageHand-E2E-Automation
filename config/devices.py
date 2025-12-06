from dataclasses import dataclass
from typing import Optional


@dataclass
class Device:
    
    name: str
    width: int
    height: int
    user_agent: Optional[str] = None
    
    def __post_init__(self):
        if self.user_agent is None:
            self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


class Mobile(Device):
    """(iPhone 15 Pro Max size)"""
    
    def __init__(self):
        super().__init__(
            name="mobile",
            width=430,
            height=932,
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            )
        )


class Ipad(Device):
    """(iPad Pro 12.9\" size)"""
    
    def __init__(self):
        super().__init__(
            name="ipad",
            width=1024,
            height=1366,
            user_agent=(
                "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            )
        )


class Desktop(Device):
    """(default 1920x1080)"""
    
    def __init__(self):
        super().__init__(
            name="desktop",
            width=1920,
            height=1080,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        )


def get_device_class(device_type: str) -> Device:
    device_type_lower = device_type.lower() if device_type else "desktop"
    
    device_map = {
        "mobile": Mobile,
        "ipad": Ipad,
        "tablet": Ipad,  # Backward compatibility
        "desktop": Desktop,
    }
    
    device_class = device_map.get(device_type_lower)
    
    if device_class is None:
        raise ValueError(
            f"Unsupported device type: {device_type}. "
            f"Supported types: {', '.join(['mobile', 'ipad', 'tablet', 'desktop'])}"
        )
    
    return device_class()

