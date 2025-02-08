#!/bin/bash

# 定義
GADGET_SCRIPT_PATH="/usr/local/bin/setup_usb_hid_gadget.sh"
SERVICE_FILE_PATH="/etc/systemd/system/setup_usb_hid_gadget.service"

echo "Stopping and disabling the USB gadget service..."

# サービスを停止
if systemctl is-active --quiet setup_usb_hid_gadget.service; then
    sudo systemctl stop setup_usb_hid_gadget.service
    echo "Service stopped."
else
    echo "Service is not running."
fi

# サービスを無効化
if systemctl is-enabled --quiet setup_usb_hid_gadget.service; then
    sudo systemctl disable setup_usb_hid_gadget.service
    echo "Service disabled."
else
    echo "Service is not enabled."
fi

# サービスファイルを削除
if [ -f "$SERVICE_FILE_PATH" ]; then
    sudo rm "$SERVICE_FILE_PATH"
    echo "Service file removed."
else
    echo "Service file not found."
fi

# コピーされたスクリプトを削除
if [ -f "$GADGET_SCRIPT_PATH" ]; then
    sudo rm "$GADGET_SCRIPT_PATH"
    echo "Gadget script removed."
else
    echo "Gadget script not found."
fi

echo "Cleanup complete."
