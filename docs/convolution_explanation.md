# Introduction
I've tried template matching to detect a double kill, but it doesn't seem to be the right approach. It was the second method tried after considering YOLO, but we don't want to make a dataset when we've already tried that, and it didn't work, and we're guessing it's not the right approach.

Template matching docs:
https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html

# Helpful explanation
Gemini ->
So it's confusing because in this explanation you havent mentioned edges, textures, etc. You're just describing several comparison operations which depending on the operation will result in the most likely matches being the brightest or darkest pixels

<-
You're absolutely right to call out the confusion. My apologies for not explicitly connecting the comparison operations back to edges, textures, etc., in the previous explanation. Let me clarify how those image features relate to the different template matching metrics:

**The Core Idea:** All these template matching methods (whether based directly on convolution or not) are trying to quantify how "similar" the template is to different parts of the image. The way they quantify this "similarity" determines how they respond to different image features.

**1. `cv.TM_SQDIFF` (Sum of Squared Differences) and `cv.TM_SQDIFF_NORMED`:**

*   **How it works:** This method calculates the sum of the squared differences between corresponding pixels in the template and the image patch. A *lower* value (darker pixel in the result image) indicates a better match.
*   **Response to features:**
    *   **Sharp edges:** If the template has a sharp edge and it aligns perfectly with a similar edge in the image, the squared differences will be small, resulting in a low score (good match). However, if the template's edge is slightly misaligned or the edge in the image is blurry, the squared differences will be larger, leading to a worse score. SQDIFF is very sensitive to pixel alignment.
    *   **Noise:** Noise (random variations in pixel values) will also increase the squared differences, making it harder to find a good match.
    *   **Color changes:** Abrupt color changes (which often correspond to edges) will affect the metric.
*   **In summary:** `SQDIFF` is very sensitive to pixel-level differences. It will give good results when the template and the matching region are nearly identical, but it's easily affected by noise, slight misalignments, and variations in lighting.

**2. `cv.TM_CCORR` (Cross-Correlation) and `cv.TM_CCORR_NORMED`:**

*   **How it works:** This method calculates the cross-correlation between the template and the image patch. A *higher* value (brighter pixel in the result image) indicates a better match.
*   **Response to features:**
    *   **Edges and textures:** If the template contains an edge or a texture pattern, and that pattern is present in the image, the cross-correlation will be high. This is because the convolution operation effectively measures how well the template's intensity pattern "matches" the image's intensity pattern.
    *   **Smooth gradients:** `CCORR` is also sensitive to smooth changes in intensity (gradients), not just sharp edges.
    *   **Lighting changes:** The normalized version (`CCORR_NORMED`) is less sensitive to global changes in lighting because it normalizes the values.
*   **In summary:** `CCORR` and `CCORR_NORMED` are more robust to noise and slight variations than `SQDIFF`. They are good at detecting patterns and are less sensitive to precise pixel alignment.

**3. `cv.TM_CCOEFF` (Correlation Coefficient) and `cv.TM_CCOEFF_NORMED`:**

*   **How it works:** This method calculates the correlation coefficient, which measures the linear relationship between the template and the image patch. A *higher* value (brighter pixel in the result image) indicates a better match.
*   **Response to features:**
    *   **Similar to CCORR:** This method is also good at detecting patterns and is robust to lighting changes (especially the normalized version). However, it's more robust to linear changes in lighting and contrast compared to `CCORR`.
*   **In summary:** `CCOEFF` and `CCOEFF_NORMED` are often considered the most robust general-purpose template matching methods.

**Connecting back to your original concern:**

When you're trying to detect a simple shape like a circle, the problem is that many other things in a 3D game environment (edges of objects, highlights, shadows, etc.) can create similar intensity patterns that the convolution (or related calculations) will respond to. This is why you get false positives. The template matching methods are designed to find *patterns*, and a simple circle doesn't provide a very distinctive pattern in terms of pixel intensities, especially against a complex background.

Using color-based segmentation and shape analysis, as previously suggested, is much more effective in this case because it directly targets the key features of the medal: its color and circular shape.
