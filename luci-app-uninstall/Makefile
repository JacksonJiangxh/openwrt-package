include $(TOPDIR)/rules.mk

PKG_NAME:=luci-app-uninstall
PKG_VERSION:=1.2.0
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/$(PKG_NAME)
  SECTION:=luci
  CATEGORY:=LuCI
  SUBMENU:=3. Applications
  TITLE:=LuCI support for Uninstall
  PKGARCH:=all
endef

define Package/$(PKG_NAME)/description
  LuCI support for Uninstall
endef

define Build/Prepare
  mkdir -p $(PKG_BUILD_DIR)
  curl -L -o $(PKG_BUILD_DIR)/luci-app-uninstall.run https://plugin.vumstar.com/download/luci-app-uninstall.run
  chmod +x $(PKG_BUILD_DIR)/luci-app-uninstall.run
  $(PKG_BUILD_DIR)/luci-app-uninstall.run --noexec --keep --target $(PKG_BUILD_DIR)
endef

define Build/Compile
endef

define Package/$(PKG_NAME)/install
  $(INSTALL_DIR) $(1)/tmp
  IPK_FILE=$$(ls $(PKG_BUILD_DIR)/luci-app-uninstall_*.ipk | head -n 1)
  IPK_FILENAME=$$(basename "$$IPK_FILE")
  $(CP) "$$IPK_FILE" $(1)/tmp/
  $(INSTALL_DIR) $(1)/usr/lib/opkg/info
  echo "echo 'Installing luci-app-uninstall...' && opkg install /tmp/$$IPK_FILENAME && rm /tmp/$$IPK_FILENAME" > $(1)/usr/lib/opkg/info/$(PKG_NAME).postinst
  chmod +x $(1)/usr/lib/opkg/info/$(PKG_NAME).postinst
endef

$(eval $(call BuildPackage,$(PKG_NAME)))
