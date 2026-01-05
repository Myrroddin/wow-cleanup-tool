"""World of Warcraft Console Variables (CVars) reference for optimization.

This module provides a structured reference of performance and graphics-related
CVars with their defaults, types, ranges, and descriptions. Used by the optimizer
to suggest configuration tweaks based on detected hardware.

Source: Wowpedia "Console variables/Complete list" (PTR client snapshot)
Last updated: December 3, 2025
"""

# Structured CVar reference organized by category
OPTIMIZATION_CVARS = {
    "frame_rate_latency": {
        "LowLatencyMode": {
            "default": 0,
            "type": "int",
            "range": [0, 1, 2],
            "description": "Low latency mode selector.",
            "values": {0: "None", 1: "BuiltIn", 2: "Reflex"},
        },
        "gxMaxFrameLatency": {
            "default": 3,
            "type": "int",
            "range": (0, 10),
            "description": "Maximum number of frames ahead of GPU the CPU can be.",
        },
        "maxFPS": {
            "default": 120,
            "type": "int",
            "range": (30, 500),
            "description": "Set FPS limit.",
        },
        "maxFPSBk": {
            "default": 30,
            "type": "int",
            "range": (10, 120),
            "description": "Set background FPS limit.",
        },
        "maxFPSLoading": {
            "default": 10,
            "type": "int",
            "range": (5, 60),
            "description": "Set loading screen max FPS.",
        },
        "vsync": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "VSync on or off.",
        },
    },
    "graphics_api_gpu_selection": {
        "gxApi": {
            "default": "auto",
            "type": "string",
            "description": "Graphics API selection.",
        },
        "gxAdapter": {
            "default": "",
            "type": "string",
            "description": "Set which GPU to use. See GxListGPUs for valid names (empty string lets the client choose).",
        },
        "gxMonitor": {
            "default": 0,
            "type": "int",
            "description": "Monitor selection.",
        },
        "gxFullscreenResolution": {
            "default": "auto",
            "type": "string",
            "description": "Fullscreen resolution selection.",
        },
        "gxWindowedResolution": {
            "default": "1920x1080",
            "type": "string",
            "description": "Windowed resolution.",
        },
        "gxNewResolution": {
            "default": "0x0",
            "type": "string",
            "description": "Resolution to be set.",
        },
        "gxAspect": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Constrain window aspect.",
        },
    },
    "render_threading": {
        "gxMTDisable": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Disable all render multithreading.",
        },
        "gxMTBeginDraw": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Do BeginDraw multithreaded.",
        },
        "gxMTPrepass": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Render prepass in parallel.",
        },
        "gxMTShadow": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Render shadow bands in parallel.",
        },
        "gxMTTerrain": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Render terrain in parallel.",
        },
        "gxMTOpaqueWMO": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Render opaque WMO in parallel.",
        },
        "gxMTOpaqueM2": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Render opaque model pass in parallel.",
        },
        "gxMTOpaqueM2NoReflect": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Render opaque model no reflection pass in parallel.",
        },
        "gxMTAlphaM2": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Render transparent M2 pass in parallel.",
        },
        "gxMTAlphaWater": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Render Alpha Water Volumes in parallel.",
        },
        "gxMTParticulateVolumes": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Render Particulate Volumes in parallel.",
        },
        "GxAllowCachelessShaderMode": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "CPU memory saving mode for shaders. When enabled, shaders are fetched from disk as needed instead of kept resident.",
        },
        "GxPrismEnabled": {
            "default": 1,
            "type": "int",
            "range": [0, 1, 2],
            "description": "Prism backends toggle.",
            "values": {0: "Disabled", 1: "Default enabled", 2: "Experimental enabled"},
        },
        "gxAftermathEnabled": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Enable frame crash debugging.",
        },
        "gxAFRDevicesCount": {
            "default": 0,
            "type": "int",
            "description": "Force set number of AFR devices.",
        },
    },
    "upscaling_resample_vrs": {
        "RenderScale": {
            "default": 1.0,
            "type": "float",
            "range": (0.5, 2.0),
            "description": "Render scale (supersampling or undersampling).",
        },
        "ResampleQuality": {
            "default": 3,
            "type": "int",
            "range": (0, 4),
            "description": "Resample quality.",
        },
        "ResampleAlwaysSharpen": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Run sharpness pass even if not using AMD FSR Upscale.",
        },
        "ResampleSharpness": {
            "default": 0.2,
            "type": "float",
            "range": (-1.0, 2.0),
            "description": "FSR sharpness strength. 0 is full strength; -1 disables.",
        },
        "vrsWorldGeo": {
            "default": "1x1",
            "type": "string",
            "description": "Render-scale-like effect for terrain, buildings, and liquids.",
        },
        "vrsParticles": {
            "default": "1x1",
            "type": "string",
            "description": "Render-scale-like effect for particles.",
        },
        "vrsValar": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Generate a shading rate mask based on velocity and luminance (requires VRS Tier 2).",
        },
        "vrsValarUseAsyncCompute": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Use async compute for VALAR.",
        },
        "vrsValarUseMotionVectors": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Use motion vectors for VALAR.",
        },
        "vrsValarUseWeberFechner": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Use Weber-Fechner algorithm for VALAR.",
        },
        "vrsValarEnvLuma": {
            "default": 0.05,
            "type": "float",
            "range": (0.0, 1.0),
            "description": "Environment luminance for VALAR.",
        },
        "vrsValarK": {
            "default": 2.13,
            "type": "float",
            "range": (0.0, 10.0),
            "description": "Quarter rate sensitivity (K) for VALAR.",
        },
        "vrsValarSensitivityThreshold": {
            "default": 0.31,
            "type": "float",
            "range": (0.0, 1.0),
            "description": "Sensitivity threshold for VALAR.",
        },
        "vrsValarWeberFechnerConstant": {
            "default": 1.0,
            "type": "float",
            "range": (0.0, 2.0),
            "description": "Weber-Fechner constant for VALAR.",
        },
    },
    "lighting_shadows_reflections": {
        "shadowMode": {
            "default": 0,
            "type": "int",
            "range": [0, 1, 2, 3],
            "description": "Quality of shadows.",
        },
        "shadowTextureSize": {
            "default": 1024,
            "type": "int",
            "range": [1024, 2048],
            "description": "Shadow texture size.",
        },
        "shadowSoft": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Soft shadows.",
        },
        "shadowBlendCascades": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Blend between shadow cascades.",
        },
        "shadowRt": {
            "default": 0,
            "type": "int",
            "range": [0, 1, 2, 3],
            "description": "Raytraced shadows.",
        },
        "shadowCull": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Enable shadow frustum culling.",
        },
        "shadowInstancing": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Enable instancing when rendering shadowmaps.",
        },
        "shadowScissor": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Enable scissoring when rendering shadowmaps.",
        },
        "SSAO": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Screen-Space Ambient Occlusion.",
        },
        "SSAOType": {
            "default": 0,
            "type": "int",
            "description": "Screen-Space Ambient Occlusion Type.",
        },
        "ssaoMagicNormals": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "SSAO uses combined GBuffer + face normals to balance architecture/foliage/characters.",
        },
        "ssaoMagicThresholdLow": {
            "default": 25,
            "type": "int",
            "range": (0, 90),
            "description": "SSAO low threshold for transitioning from gbuffer to face normal (degrees).",
        },
        "ssaoMagicThresholdHigh": {
            "default": 50,
            "type": "int",
            "range": (0, 90),
            "description": "SSAO high threshold for transitioning from gbuffer to face normal (degrees).",
        },
        "reflectionMode": {
            "default": 3,
            "type": "int",
            "description": "Reflection mode.",
        },
        "reflectionDownscale": {
            "default": 0,
            "type": "int",
            "description": "Reflection downscale.",
        },
        "rippleDetail": {
            "default": 2,
            "type": "int",
            "description": "Ripple surface detail.",
        },
        "waterDetail": {
            "default": 0,
            "type": "int",
            "description": "Water surface detail.",
        },
        "volumeFog": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Volume Fog.",
        },
        "volumeFogInterior": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Volume Fog Interiors.",
        },
        "volumeFogLevel": {
            "default": 2,
            "type": "int",
            "range": [0, 1, 2, 3],
            "description": "Volume Fog Level.",
        },
        "specular": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Specular lighting multiplier.",
        },
    },
    "lod_view_distance": {
        "terrainLodDist": {
            "default": 400,
            "type": "int",
            "range": (100, 1000),
            "description": "Terrain level of detail distance.",
        },
        "TerrainLodDiv": {
            "default": 768,
            "type": "int",
            "description": "Terrain LOD divisor.",
        },
        "terrainMipLevel": {
            "default": 0,
            "type": "int",
            "range": (0, 5),
            "description": "Terrain blend map mip level.",
        },
        "horizonClip": {
            "default": 1600,
            "type": "int",
            "description": "Horizon clip distance.",
        },
        "horizonStart": {
            "default": 800,
            "type": "int",
            "description": "Horizon start distance.",
        },
        "lodObjectCullDist": {
            "default": 30,
            "type": "int",
            "description": "LOD object culling distance minimum.",
        },
        "lodObjectCullSize": {
            "default": 15,
            "type": "int",
            "description": "LOD object culling size.",
        },
        "lodObjectFadeScale": {
            "default": 100,
            "type": "int",
            "description": "LOD object fade scale.",
        },
        "lodObjectMinSize": {
            "default": 20,
            "type": "int",
            "description": "LOD object min size.",
        },
        "lodObjectSizeScale": {
            "default": 1,
            "type": "int",
            "description": "Scales all objects size for culling.",
        },
    },
    "particles_clutter_density": {
        "groundEffectDensity": {
            "default": 16,
            "type": "int",
            "range": (0, 100),
            "description": "Ground effect density.",
        },
        "groundEffectDist": {
            "default": 70,
            "type": "int",
            "range": (10, 200),
            "description": "Ground effect distance.",
        },
        "groundEffectFade": {
            "default": 70,
            "type": "int",
            "range": (10, 200),
            "description": "Ground effect fade.",
        },
        "particleDensity": {
            "default": 100,
            "type": "int",
            "range": (0, 100),
            "description": "Particle density.",
        },
        "particleMTDensity": {
            "default": 100,
            "type": "int",
            "range": (0, 100),
            "description": "Multi-Tex particle density.",
        },
        "particulatesEnabled": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Particulates enabled.",
        },
        "spellClutter": {
            "default": -1,
            "type": "int",
            "range": (-1, 100),
            "description": "Cull unimportant spell effects. -1=auto based on targetFPS; 0=cull nothing; 100=cull as much as possible.",
        },
    },
    "cpu_affinity_threading": {
        "processAffinityMask": {
            "default": 0,
            "type": "int",
            "description": "Sets which core(s) WoW may execute on (requires restart to take effect).",
        },
        "occlusionMaxJobs": {
            "default": 5,
            "type": "int",
            "range": (1, 64),
            "description": "Maximum job threads for occlusion render.",
        },
        "locateViewerMaxJobs": {
            "default": 32,
            "type": "int",
            "range": (1, 64),
            "description": "Maximum job threads for LocateViewer.",
        },
        "worldViewCullMaxJobs": {
            "default": 32,
            "type": "int",
            "range": (1, 64),
            "description": "Maximum job threads for culling.",
        },
        "hwDetect": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Do hardware detection.",
        },
    },
    "streaming_preload": {
        "worldPreloadNonCritical": {
            "default": 2,
            "type": "int",
            "description": "Require objects to be loaded in streaming non critical radius when preloading.",
        },
        "worldPreloadNonCriticalTimeout": {
            "default": 45,
            "type": "int",
            "range": (10, 120),
            "description": "World preload time (seconds) when non-critical items are automatically ignored.",
        },
        "worldPreloadSort": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Sort objects by distance when preloading.",
        },
        "streamingCameraLookAheadTime": {
            "default": 2000,
            "type": "int",
            "range": (500, 5000),
            "description": "Look-ahead time for streaming (milliseconds).",
        },
        "streamingCameraMaxRadius": {
            "default": 250,
            "type": "int",
            "range": (100, 500),
            "description": "Max radius of the streaming camera.",
        },
        "teleportMaxNoLoadDist": {
            "default": 200,
            "type": "int",
            "range": (50, 500),
            "description": "Max teleport distance without preload.",
        },
    },
    "ui_graphics_presets": {
        "graphicsQuality": {
            "default": 6,
            "type": "int",
            "description": "Save for Graphics Quality Selection.",
        },
        "graphicsViewDistance": {
            "default": 6,
            "type": "int",
            "description": "UI value of the graphics setting.",
        },
        "graphicsTextureResolution": {
            "default": 2,
            "type": "int",
            "description": "UI value of the graphics setting.",
        },
        "graphicsShadowQuality": {
            "default": 3,
            "type": "int",
            "description": "UI value of the graphics setting.",
        },
        "graphicsSSAO": {
            "default": 3,
            "type": "int",
            "description": "UI value of the graphics setting.",
        },
        "graphicsSpellDensity": {
            "default": 4,
            "type": "int",
            "description": "UI value of the graphics setting.",
        },
        "graphicsProjectedTextures": {
            "default": 1,
            "type": "int",
            "description": "UI value of the graphics setting.",
        },
    },
    "raid_graphics_presets": {
        "raidGraphicsViewDistance": {
            "default": 6,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "raidGraphicsTextureResolution": {
            "default": 2,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "raidGraphicsShadowQuality": {
            "default": 3,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "raidGraphicsSSAO": {
            "default": 3,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "raidGraphicsSpellDensity": {
            "default": 4,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "raidGraphicsParticleDensity": {
            "default": 4,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "raidGraphicsLiquidDetail": {
            "default": 2,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "raidGraphicsGroundClutter": {
            "default": 6,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "raidGraphicsProjectedTextures": {
            "default": 1,
            "type": "int",
            "description": "UI value of the raidGraphics setting.",
        },
        "RAIDgraphicsQuality": {
            "default": 6,
            "type": "int",
            "description": "Save for Raid Graphics Quality Selection.",
        },
        "RAIDspellClutter": {
            "default": -1,
            "type": "int",
            "range": (-1, 100),
            "description": "Cull unimportant spell effects (raid). -1=auto based on targetFPS; 0=cull nothing; 100=cull as much as possible.",
        },
        "RAIDshadowTextureSize": {
            "default": 1024,
            "type": "int",
            "range": [1024, 2048],
            "description": "Shadow texture size (raid).",
        },
        "RAIDVolumeFog": {
            "default": 0,
            "type": "int",
            "range": [0, 1],
            "description": "Volume Fog (raid).",
        },
        "RAIDVolumeFogLevel": {
            "default": 2,
            "type": "int",
            "range": [0, 1, 2, 3],
            "description": "Volume Fog Level (raid).",
        },
        "RAIDterrainLodDist": {
            "default": 400,
            "type": "int",
            "range": (100, 1000),
            "description": "Terrain LOD distance (raid).",
        },
        "RAIDterrainMipLevel": {
            "default": 0,
            "type": "int",
            "range": (0, 5),
            "description": "Terrain blend map mip level (raid).",
        },
    },
    "other_toggles": {
        "M2UseInstancing": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Use hardware instancing.",
        },
        "M2UseThreads": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Multithread model animations.",
        },
        "sceneOcclusionEnable": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Scene software occlusion.",
        },
        "MSAAAlphaTest": {
            "default": 1,
            "type": "int",
            "range": [0, 1],
            "description": "Enable MSAA for alpha-tested geometry.",
        },
        "MSAAQuality": {
            "default": 0,
            "type": "int",
            "description": "Multisampling AA quality.",
        },
    },
}


def get_cvar(cvar_name: str) -> dict | None:
    """Look up a CVar by name across all categories.

    Args:
        cvar_name: Name of the CVar to look up

    Returns:
        CVar definition dict, or None if not found
    """
    for category_cvars in OPTIMIZATION_CVARS.values():
        if cvar_name in category_cvars:
            return category_cvars[cvar_name]
    return None


def get_cvars_by_category(category: str) -> dict:
    """Get all CVars in a specific category.

    Args:
        category: Category name (key in OPTIMIZATION_CVARS)

    Returns:
        Dictionary of CVars in that category, or empty dict if not found
    """
    return OPTIMIZATION_CVARS.get(category, {})


def list_categories() -> list[str]:
    """List all available CVar categories.

    Returns:
        List of category names
    """
    return list(OPTIMIZATION_CVARS.keys())
