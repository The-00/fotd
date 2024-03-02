from nicegui import ui, Client
import os


def balises(name, image_path, page_path):

    website = os.environ['WEBSITE']

    name  = name.replace('"', '\\"') 
    image = website + image_path.replace('"', '\\"') 
    page  = website + page_path.replace('"', '\\"') 

    ui.add_head_html(f'''
    <meta name="description" content="Frog Of The Day">

    <!-- Google / Search Engine Tags -->
    <meta itemprop="name" content="FOTD | {name}">
    <meta itemprop="description" content="Frog Of The Day">
    <meta itemprop="image" content="{image}">

    <!-- Facebook Meta Tags -->
    <meta property="og:url" content="{page}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="FOTD | {name}">
    <meta property="og:description" content="Frog Of The Day">
    <meta property="og:image" content="{image}">

    <!-- Twitter Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="FOTD | {name}">
    <meta name="twitter:description" content="Frog Of The Day">
    <meta name="twitter:image" content="{image}">
    ''')