#!/bin/bash

# 定義
GADGET_SCRIPT_PATH="/usr/local/bin/setup_usb_hid_gadget.sh"
SERVICE_FILE_PATH="/etc/systemd/system/setup_usb_hid_gadget.service"

# 既存のUSBガジェットスクリプトをコピー
echo "Copying USB gadget script to $GADGET_SCRIPT_PATH..."
sudo cp ./setup_usb_hid_gadget.sh "$GADGET_SCRIPT_PATH"
sudo chmod +x "$GADGET_SCRIPT_PATH"

# systemdサービスファイルを作成
echo "Creating systemd service file at $SERVICE_FILE_PATH..."
sudo bash -c "cat > $SERVICE_FILE_PATH" <<EOL
[Unit]
Description=Setup USB Gadget Mode
After=network.target sys-kernel-config.mount

[Service]
Type=oneshot
ExecStart=$GADGET_SCRIPT_PATH
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOL

# サービスを有効化
echo "Enabling the systemd service..."
sudo systemctl enable setup_usb_hid_gadget.service

# サービスを起動して確認
echo "Starting the service to test..."
sudo systemctl start setup_usb_hid_gadget.service
sudo systemctl status setup_usb_hid_gadget.service
