"""UI constants for dialog dimensions and styling."""


class DialogDimensions:
    """Standard dialog dimensions and spacing."""
    
    # Dialog minimum sizes
    MIN_LICENSE_WIDTH = 700
    MIN_LICENSE_HEIGHT = 500
    
    MIN_WARNING_WIDTH = 500
    MIN_WARNING_HEIGHT = 300
    
    MIN_SIMPLE_WARNING_WIDTH = 450
    MIN_SIMPLE_WARNING_HEIGHT = 250
    
    # Standard padding
    CONTENT_PADDING = 20
    FRAME_PADDING = 10
    BUTTON_PADDING = 5
    
    # Standard button widths
    BUTTON_WIDTH_STANDARD = 15
    BUTTON_WIDTH_NARROW = 10
    BUTTON_WIDTH_WIDE = 20
    
    # Text wrapping lengths
    WRAP_SHORT = 380
    WRAP_MEDIUM = 450
    WRAP_LONG = 650
    
    # Spacing
    SPACING_SMALL = 5
    SPACING_MEDIUM = 10
    SPACING_LARGE = 15
    SPACING_XLARGE = 20


class DialogFontSizes:
    """Font size offsets for dialog elements relative to base font size."""
    
    # Offsets from base font size
    TITLE_OFFSET = 3
    SUBTITLE_OFFSET = 2
    WARNING_ICON_OFFSET = 15  # For large warning symbols
    
    @staticmethod
    def get_title_size(base_size):
        """Get title font size.
        
        Args:
            base_size: Base font size
            
        Returns:
            int: Title font size
        """
        return base_size + DialogFontSizes.TITLE_OFFSET
    
    @staticmethod
    def get_subtitle_size(base_size):
        """Get subtitle font size.
        
        Args:
            base_size: Base font size
            
        Returns:
            int: Subtitle font size
        """
        return base_size + DialogFontSizes.SUBTITLE_OFFSET
    
    @staticmethod
    def get_icon_size(base_size):
        """Get warning icon font size.
        
        Args:
            base_size: Base font size
            
        Returns:
            int: Icon font size
        """
        return base_size + DialogFontSizes.WARNING_ICON_OFFSET
