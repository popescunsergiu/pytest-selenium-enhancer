# pylint: disable=import-outside-toplevel
# pylint: disable=no-member


def compare_images(image_b, base_screenshot_url, actual_screenshot_url, diff_screenshot_url, base_score=1):
    from skimage.measure import compare_ssim
    from os import makedirs
    import imutils
    import cv2

    # load the two input images
    image_a = cv2.imread(base_screenshot_url)

    if image_a is None:
        makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        cv2.imwrite(actual_screenshot_url, image_b)
        raise AssertionError('There is no base image for: %s' % base_screenshot_url)

    # convert the images to grayscale
    gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    if gray_a.shape != gray_b.shape:
        makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        cv2.imwrite(actual_screenshot_url, image_b)
        raise AssertionError(
            'Base: %s and\n Actual: %s\n have different sized' % (base_screenshot_url, actual_screenshot_url))

    (score, diff) = compare_ssim(gray_a, gray_b, full=True)
    if score < base_score:
        makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        makedirs(diff_screenshot_url[:diff_screenshot_url.rfind('/')], exist_ok=True)
        cv2.imwrite(actual_screenshot_url, image_b)
        diff = (diff * 255).astype("uint8")

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for cnt in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x_point, y_point, width, height) = cv2.boundingRect(cnt)
            cv2.rectangle(image_b, (x_point, y_point), (x_point + width, y_point + height), (0, 0, 255), 2)

        cv2.imwrite(diff_screenshot_url, image_b)

    return score
