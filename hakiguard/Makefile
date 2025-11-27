include $(TOPDIR)/rules.mk

PKG_NAME:=hakiguard
PKG_VERSION:=1.0.0
PKG_RELEASE:=1

PKG_LICENSE:=MIT
PKG_MAINTAINER:=Rodrigo Schwartzhaupt Nunes

include $(INCLUDE_DIR)/package.mk

define Package/hakiguard
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=HakiGuard AI Security Module
  DEPENDS:=+python3 +python3-light +python3-json
endef

define Package/hakiguard/description
  HakiGuard is a lightweight AI-based traffic inspection module
  using UNIX sockets for real-time communication with OpenWRT.
endef

define Build/Compile
    # Não compila nada, pois é Python
endef

define Package/hakiguard/install
	$(INSTALL_DIR) $(1)/usr/lib/hakiguard/bridge
	$(INSTALL_DIR) $(1)/usr/lib/hakiguard/listener
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_DIR) $(1)/var/run

	$(INSTALL_BIN) ./files/usr/lib/hakiguard/bridge/send_result.py \
		$(1)/usr/lib/hakiguard/bridge/send_result.py

	$(INSTALL_BIN) ./files/usr/lib/hakiguard/listener/hakiguard-listener.py \
		$(1)/usr/lib/hakiguard/listener/hakiguard-listener.py

	$(INSTALL_BIN) ./files/etc/init.d/hakiguard \
		$(1)/etc/init.d/hakiguard
endef

$(eval $(call BuildPackage,hakiguard))

