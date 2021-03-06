pkgname=rflink-mqtt2mqtt-git
pkgver=0.1
pkgrel=1
pkgdesc="Simple RFLink MQTT to MQTT bridge"
arch=('any')
url="https://github.com/andyboeh/rflink-mqtt2mqtt"
license=('GPL')
depends=('python' 'python-paho-mqtt')
install='rflink-mqtt2mqtt.install'
source=('rflink-mqtt2mqtt-git::git+https://github.com/andyboeh/rflink-mqtt2mqtt.git'
        'rflink-mqtt2mqtt.install'
        'rflink-mqtt2mqtt.sysusers'
        'rflink-mqtt2mqtt.service')
provides=('rflink-mqtt2mqtt')
conflicts=('rflink-mqtt2mqtt')
sha256sums=('SKIP'
            '20f066f231ade8a9e3c2e688efb386c6cf4ba1dc86e4eb0a72cb9bf3ef91a08a'
            '997da4afe9598f5569d6ca9db5469cc2011c9b70477977eb1f660d9e1ef7cbb1'
            'e1baa9d227be74e7ccef0e36c6d829bb9cc6ebd64a8f087b2b0651780a7086f8')
backup=('opt/rflink-mqtt2mqtt/rflink-mqtt2mqtt.yaml')

pkgver() {
  cd "$pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
  cd "${pkgname}"
  install -d "${pkgdir}/opt/rflink-mqtt2mqtt"
  cp rflink-mqtt2mqtt.py "${pkgdir}/opt/rflink-mqtt2mqtt/rflink-mqtt2mqtt.py"
  install -Dm644 "${srcdir}/rflink-mqtt2mqtt.service" "${pkgdir}/usr/lib/systemd/system/rflink-mqtt2mqtt.service"
  install -Dm644 "${srcdir}/rflink-mqtt2mqtt.sysusers" "${pkgdir}/usr/lib/sysusers.d/rflink-mqtt2mqtt.conf"
  install -Dm644 rflink-mqtt2mqtt.yaml "${pkgdir}/opt/rflink-mqtt2mqtt/rflink-mqtt2mqtt.yaml"
}
