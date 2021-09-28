from PIL import Image
from io import BytesIO
from modules.helpers import check_dir
from playwright.sync_api import sync_playwright


config = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "viewport": {
        "width": 1920,
        "height": 1080
    },
    "color-scheme": "dark"
}

def unit_list(module_url):
    unit_urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            user_agent=config["user-agent"],
            viewport=config["viewport"],
            color_scheme=config["color-scheme"]
        )
        page = context.new_page()
        page.goto(module_url)
        anchor_list = page.query_selector("#unit-list").query_selector_all("a")

        for a in range(len(anchor_list)):
            href = anchor_list[a].get_attribute("href")
            merged_url = str(module_url) + str(href)
            unit_urls.append(merged_url)

        browser.close()

    return unit_urls

def module_name(module_url):
    name = ""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            user_agent=config["user-agent"],
            viewport=config["viewport"],
            color_scheme=config["color-scheme"]
        )
        page = context.new_page()
        page.goto(module_url)

        header_element = page.query_selector("#main > div.modular-content-container > div > div > div > div > div > div.columns.is-mobile.is-gapless.has-margin-bottom-none > div > h1")
        sanitize_name = str(header_element.inner_text()).lower().replace(" ", "-")
        name = sanitize_name

        browser.close()

    return name

def build_dir(module_url, export_dir):
    project_name = module_name(module_url)
    project_dir = f"{export_dir}\\{project_name}"

    check_dir(project_dir)

    return project_dir

def screenshot_unit(unit_url):
    image_bytes = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            user_agent=config["user-agent"],
            viewport=config["viewport"],
            color_scheme=config["color-scheme"]
        )
        page = context.new_page()
        page.goto(unit_url)

        element_handle = page.query_selector("#unit-inner-section")
        image_bytes = element_handle.screenshot()

        browser.close()

    return image_bytes

def concat_image_vertically(image_one, image_two, color=(0, 0, 0)):
    pil_image_one = Image.open(BytesIO(image_one))
    pil_image_two = Image.open(BytesIO(image_two))

    base = Image.new("RGB", (max(pil_image_one.width, pil_image_two.width), pil_image_one.height + pil_image_two.height), color)

    base.paste(pil_image_one, (0, 0))
    base.paste(pil_image_two, (0, pil_image_one.height))

    image_byte_array = BytesIO()
    base.save(image_byte_array, format="PNG")
    image_byte_array = image_byte_array.getvalue()

    return image_byte_array

def merge_image_files(byte_image_list):
    init_image = byte_image_list[0]

    for image in range(1, len(byte_image_list)):
        init_image = concat_image_vertically(init_image, byte_image_list[image])

    return init_image

def ms_learn(module_url, export_dir):
    project_name = ""
    project_dir = f"{export_dir}\\"
    unit_urls = []
    byte_images = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            user_agent=config["user-agent"],
            viewport=config["viewport"],
            color_scheme=config["color-scheme"]
        )
        page = context.new_page()
        page.goto(module_url)

        # JOB: Extract project name from header + Build output directory from project name
        header_element = page.query_selector("#main > div.modular-content-container > div > div > div > div > div > div.columns.is-mobile.is-gapless.has-margin-bottom-none > div > h1")
        sanitize_name = str(header_element.inner_text()).lower().replace(" ", "-")
        project_name = sanitize_name
        project_dir = project_dir + project_name

        # JOB: Required directory check
        check_dir(project_dir)

        # JOB: Build list of unit URLs
        anchor_list = page.query_selector("#unit-list").query_selector_all("a")

        for a in range(len(anchor_list)):
            href = anchor_list[a].get_attribute("href")
            merged_url = str(module_url) + str(href)
            unit_urls.append(merged_url)

        # JOB: Save screenshot as byte_array + Create list of byte_array images
        for unit in range(len(unit_urls)):
            page.goto(unit_urls[unit])
            element_handle = page.query_selector("#unit-inner-section")
            image_bytes = element_handle.screenshot()
            byte_images.append(image_bytes)

        browser.close()

    # JOB: Combine byte_array images + Return image/png save location
    merged_image = Image.open(BytesIO(merge_image_files(byte_images)))
    save_location = f"{project_dir}\\final.png"
    merged_image.save(save_location, "PNG")

    return save_location
