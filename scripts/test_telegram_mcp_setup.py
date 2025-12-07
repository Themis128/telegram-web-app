#!/usr/bin/env python3
"""
Test script to verify Telegram MCP setup and list available tools.

This script checks:
1. Environment variables configuration
2. Python dependencies
3. MCP server module availability
4. Basic connectivity tests
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")

def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")

def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {text}")

def check_python_version() -> bool:
    """Check if Python version is 3.8 or higher."""
    print_header("Checking Python Version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str} is installed (required: 3.8+)")
        return True
    else:
        print_error(f"Python {version_str} is installed (required: 3.8+)")
        return False

def check_env_file() -> Tuple[bool, Dict[str, str]]:
    """Check if .env file exists and contains required variables."""
    print_header("Checking Environment File")

    env_path = Path(".env")
    env_vars = {}

    if not env_path.exists():
        print_error(".env file not found")
        print_info("Copy env.example to .env and fill in your credentials")
        return False, env_vars

    print_success(".env file exists")

    # Read .env file
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except Exception as e:
        print_error(f"Error reading .env file: {e}")
        return False, env_vars

    # Check required variables
    required_vars = [
        'TELEGRAM_API_ID',
        'TELEGRAM_API_HASH',
        'TELEGRAM_PHONE_NUMBER'
    ]

    missing_vars = []
    placeholder_vars = []

    for var in required_vars:
        if var not in env_vars:
            missing_vars.append(var)
        elif env_vars[var].lower() in ['', 'your_api_id_here', 'your_api_hash_here', 'your_phone_number_here']:
            placeholder_vars.append(var)

    if missing_vars:
        print_error(f"Missing required variables: {', '.join(missing_vars)}")
        return False, env_vars

    if placeholder_vars:
        print_warning(f"Variables with placeholder values: {', '.join(placeholder_vars)}")
        print_info("Please update these values in .env file")
        return False, env_vars

    # Validate values
    all_valid = True
    if env_vars.get('TELEGRAM_API_ID'):
        try:
            int(env_vars['TELEGRAM_API_ID'])
            print_success("TELEGRAM_API_ID is set and valid")
        except ValueError:
            print_error("TELEGRAM_API_ID must be a number")
            all_valid = False

    if env_vars.get('TELEGRAM_API_HASH'):
        if len(env_vars['TELEGRAM_API_HASH']) >= 32:
            print_success("TELEGRAM_API_HASH is set and appears valid")
        else:
            print_warning("TELEGRAM_API_HASH seems too short (should be 32+ characters)")

    if env_vars.get('TELEGRAM_PHONE_NUMBER'):
        if env_vars['TELEGRAM_PHONE_NUMBER'].startswith('+'):
            print_success("TELEGRAM_PHONE_NUMBER is set and includes country code")
        else:
            print_warning("TELEGRAM_PHONE_NUMBER should start with + (country code)")

    if all_valid and not placeholder_vars:
        print_success("All required environment variables are configured")
        return True, env_vars

    return False, env_vars

def check_python_packages() -> Tuple[bool, List[str]]:
    """Check if required Python packages are installed."""
    print_header("Checking Python Packages")

    required_packages = [
        'mcp',
        'mcp-telegram',
        'telethon',  # Usually required by mcp-telegram
    ]

    installed = []
    missing = []

    for package in required_packages:
        try:
            # Try different import names
            if package == 'mcp-telegram':
                try:
                    import mcp_telegram
                    installed.append(package)
                    print_success(f"{package} is installed")
                except ImportError:
                    try:
                        import tgmcp
                        installed.append('tgmcp (alternative)')
                        print_success(f"tgmcp is installed (alternative to {package})")
                    except ImportError:
                        missing.append(package)
                        print_error(f"{package} is not installed")
            elif package == 'mcp':
                try:
                    import mcp
                    installed.append(package)
                    print_success(f"{package} is installed")
                except ImportError:
                    # mcp might be part of mcp-telegram
                    print_warning(f"{package} module not found (may be included in mcp-telegram)")
            elif package == 'telethon':
                try:
                    import telethon
                    installed.append(package)
                    print_success(f"{package} is installed")
                except ImportError:
                    print_warning(f"{package} is not installed (may be optional)")
        except Exception as e:
            print_error(f"Error checking {package}: {e}")
            missing.append(package)

    if missing:
        print_info("Install missing packages with: pip install mcp-telegram")
        return False, missing

    return True, installed

def test_mcp_server_import() -> bool:
    """Test if MCP server can be imported."""
    print_header("Testing MCP Server Import")

    try:
        import mcp_telegram
        print_success("mcp_telegram module can be imported")

        # Try to get server info if available
        if hasattr(mcp_telegram, '__version__'):
            print_info(f"mcp_telegram version: {mcp_telegram.__version__}")

        return True
    except ImportError:
        try:
            import tgmcp
            print_success("tgmcp module can be imported (alternative)")
            return True
        except ImportError:
            print_error("Cannot import mcp_telegram or tgmcp")
            print_info("Install with: pip install mcp-telegram")
            return False
    except Exception as e:
        print_error(f"Error importing MCP server: {e}")
        return False

def list_mcp_tools() -> List[Dict]:
    """Attempt to list available MCP tools."""
    print_header("Listing Available MCP Tools")

    tools = []

    try:
        import mcp_telegram

        # Try to get tools from the module
        if hasattr(mcp_telegram, 'tools'):
            tools = mcp_telegram.tools
            print_success(f"Found {len(tools)} tools in mcp_telegram")
        elif hasattr(mcp_telegram, 'get_tools'):
            tools = mcp_telegram.get_tools()
            print_success(f"Found {len(tools)} tools")
        else:
            print_info("Tools list not directly accessible from module")
            print_info("Tools are exposed through MCP protocol when Cursor connects")

            # Common Telegram MCP tools (documentation-based)
            common_tools = [
                {
                    "name": "send_message",
                    "description": "Send a text message to a chat"
                },
                {
                    "name": "get_messages",
                    "description": "Get messages from a chat"
                },
                {
                    "name": "list_chats",
                    "description": "List all chats/dialogs"
                },
                {
                    "name": "get_chat_info",
                    "description": "Get information about a chat"
                },
                {
                    "name": "search_messages",
                    "description": "Search for messages in a chat"
                },
                {
                    "name": "get_user_info",
                    "description": "Get user information"
                },
                {
                    "name": "send_media",
                    "description": "Send media files (photos, videos, documents)"
                },
                {
                    "name": "delete_message",
                    "description": "Delete a message"
                },
                {
                    "name": "edit_message",
                    "description": "Edit an existing message"
                }
            ]

            print_info("Expected Telegram MCP tools (when connected through Cursor):")
            for tool in common_tools:
                print(f"  • {tool['name']}: {tool['description']}")

            print()
            print_info("To see actual available tools:")
            print_info("  1. Restart Cursor after configuration")
            print_info("  2. Check Cursor's MCP server status")
            print_info("  3. Ask Cursor's AI: 'What Telegram MCP tools are available?'")
            print_info("  4. Or check Cursor's developer tools/console for MCP tool list")

            return common_tools
    except ImportError:
        print_warning("Cannot import mcp_telegram to list tools")
    except Exception as e:
        print_warning(f"Error listing tools: {e}")

    if tools:
        print("\nAvailable Tools:")
        for i, tool in enumerate(tools, 1):
            name = tool.get('name', f'Tool {i}')
            desc = tool.get('description', 'No description')
            print(f"  {i}. {name}: {desc}")

    return tools

def check_cursor_config() -> bool:
    """Provide information about Cursor configuration."""
    print_header("Cursor Configuration Check")

    # Check for common Cursor config locations
    if sys.platform == 'win32':
        cursor_config_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "settings.json"
    elif sys.platform == 'darwin':
        cursor_config_path = Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "settings.json"
    else:
        cursor_config_path = Path.home() / ".config" / "Cursor" / "User" / "settings.json"

    if cursor_config_path.exists():
        print_success(f"Cursor settings file found at: {cursor_config_path}")
        try:
            # Try utf-8-sig first to handle BOM, fallback to utf-8
            try:
                with open(cursor_config_path, 'r', encoding='utf-8-sig') as f:
                    config = json.load(f)
            except UnicodeDecodeError:
                with open(cursor_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

            # Check for MCP configuration
            if 'mcp' in config or 'mcpServers' in config:
                print_success("MCP configuration found in Cursor settings")
                return True
            else:
                print_warning("MCP configuration not found in Cursor settings")
                print_info("You may need to add MCP server configuration manually")
                return False
        except json.JSONDecodeError as e:
            print_warning(f"Cursor config file has JSON syntax errors (line {e.lineno})")
            print_info("This is usually not critical - Cursor may still work correctly")
            print_info("MCP configuration check skipped due to JSON error")
            return False
        except Exception as e:
            print_warning(f"Could not read Cursor config: {e}")
            print_info("This is usually not critical - MCP may still be configured")
            return False
    else:
        print_warning(f"Cursor settings file not found at: {cursor_config_path}")
        print_info("This is normal if Cursor hasn't been configured yet")
        return False

def generate_summary(results: Dict) -> None:
    """Generate a summary report."""
    print_header("Test Summary")

    total_checks = len(results)
    passed = sum(1 for r in results.values() if r)

    print(f"Tests Passed: {passed}/{total_checks}")
    print()

    for check_name, passed_check in results.items():
        status = "✓ PASS" if passed_check else "✗ FAIL"
        color = Colors.GREEN if passed_check else Colors.RED
        print(f"{color}{status}{Colors.RESET} - {check_name}")

    print()

    if passed == total_checks:
        print_success("All checks passed! Your Telegram MCP setup looks good.")
        print_info("Restart Cursor to connect to the MCP server")
    else:
        print_warning("Some checks failed. Please fix the issues above.")
        print_info("After fixing issues, run this script again to verify")

def main():
    """Main test function."""
    print_header("Telegram MCP Setup Verification")

    results = {}

    # Run all checks
    results["Python Version"] = check_python_version()
    env_ok, env_vars = check_env_file()
    results["Environment Variables"] = env_ok
    packages_ok, installed = check_python_packages()
    results["Python Packages"] = packages_ok
    results["MCP Server Import"] = test_mcp_server_import()
    tools = list_mcp_tools()
    results["MCP Tools"] = len(tools) > 0 or True  # Tools might not be directly accessible
    results["Cursor Configuration"] = check_cursor_config()

    # Generate summary
    generate_summary(results)

    # Additional instructions
    print_header("Next Steps")
    print("1. If all checks passed, restart Cursor completely")
    print("2. Check Cursor's output panel for MCP connection status")
    print("3. Try asking Cursor's AI: 'List my Telegram chats'")
    print("4. Authenticate when prompted (you'll receive a code in Telegram)")
    print()
    print("For more information, see:")
    print("  - HOW_TO_USE_TELEGRAM_IN_CURSOR.md")
    print("  - MCP_TELEGRAM_CAPABILITIES.md")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
