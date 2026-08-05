# WFSC
A custom Discord welcomer bot built for the AISC server

## Overview

WFSC (Welcomer For Secret Community) is a dedicated Discord bot built for the **AI Student Community (AISC)** server. Inspired by popular Discord welcomer bot, it automates user onboarding by dynamically fetching user avatars, overlaying circular masked profile frames onto a custom-rendered banner graphic, calculating dynamic font placement, and broadcasting greeting templates to designated channels.

## Preview

When a new member joins the server, the bot dynamically outputs a personalized welcome card alongside an onboarding message:

```text
Welcome to the official AISC server @Username! 🎉

Please verify to access all channels.
Please introduce yourself in #introductions and check out #roles to get more roles.
Feel free to DM @Admin for any queries.
Please remember this is a SFW community. Make sure to review our #rules.

Enjoy your stay here, and Keep AISC-ing! 🚀
```

## Features

* **Dynamic Banner Generation:** Uses `Pillow` (PIL) to download background templates and user profile pictures, rendering a circular masked avatar with custom borders and centered text.
* **Presence Rotation:** Automated `@tasks.loop` cycling through custom bot activity statuses.
* **Channel & Role Integration:** Formats native Discord mention tokens (`<#ID>`, `<@ID>`, `<id:customize>`) inside welcoming announcements.
* **Admin Verification Command:** Built-in `wtest` administrative command restricted by User ID validation for instant visual testing.
* **Cross-Platform Font Fallbacks:** Automatically attempts to load local TrueType fonts across Termux/Linux environments, Windows paths, and PIL system defaults.

## Installation

### Requirements

* Python
* A registered Discord Bot Application with **Server Members Intent** and **Message Content Intent** enabled in the [Discord Developer Portal](https://discord.com/developers/applications).

### Step 1: Clone the Repository

```bash
git clone https://github.com/Bytex86/WFSC.git
cd WFSC
```

### Step 2: Install Dependencies

Install all required dependencies using the requirements.txt file included in the repository:

```bash
pip install -r requirements.txt
```

## Setup & Configuration

Open the main Python script (main.py) and update the top configuration section with your server specifics:

```python
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Discord Channel & Admin IDs
WELCOME_CHANNEL_ID = 
INTRO_CHANNEL_ID   = 
RULES_CHANNEL_ID   = 
ADMIN_ID           = 

# Image Layout Coordinates
BACKGROUND_URL = "https://raw.githubusercontent.com/outlawishhh/WFSC/refs/heads/main/image.png"
AVATAR_X = 412
AVATAR_Y = 270
TEXT_Y   = 500
FONT_SIZE = 60

```

### Running the Bot

Execute the script to start listening for join events:

```bash
python bot.py

```

## Usage

### Commands

* **`wtest`**: *(Admin Only)* Generates a test banner card and sends the complete onboarding message in the current channel.
* *Access:* Restricted to the user ID configured under `ADMIN_ID`. Non-admins receive an `Error 404` notice.



## How It Works

1. **Member Join Listener:** Listens for `on_member_join` events broadcasted by the Discord Gateway.
2. **Asynchronous Asset Retrieval:** Uses `aiohttp` to asynchronously fetch the remote background asset and high-resolution member avatar image buffers simultaneously.
3. **Canvas Composition:** Applies a circular alpha mask over the avatar, adds a dynamic white border, pastes it at defined offset coordinates (`AVATAR_X`, `AVATAR_Y`), and centers the user's username string along the horizontal axis.
4. **Buffer Transmission:** Saves the rendered canvas into memory via `io.BytesIO` and attaches it directly as a `discord.File` object without writing temporary files to disk.

## Credits

* **Author:** Outlawishhh
* **Target Community:** Built specifically for the **AISC** (AI Student Community) server.

## License

Copyright (C) 2026 Outlawishhh

Licensed under the GNU General Public License v3.0 (GPL-3.0).

You are free to use, modify, and redistribute this project under the terms of the GPL-3.0 license. Any distributed modifications must also remain open source and retain attribution to the original author.

See the LICENSE file for details.
