import gatt

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        device_information_service = next(
            s for s in self.services
            if s.uuid == '0000c0c0-0000-1000-8000-00805f9b34fb')

        relay_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == '0000c0c1-0000-1000-8000-00805f9b34fb')

        relay_characteristic.write_value(bytearray(b'\x01'))

        relay_characteristic.read_value()


    def characteristic_value_updated(self, characteristic, value):
        print(str(characteristic)+", value: "+value.decode("utf-8"))

    def characteristic_write_value_succeeded(self, characteristic):
        print("Write successful.")

    def characteristic_write_value_failed(self, characteristic, error):
        print("Write failed. "+str(error))


device = AnyDevice(mac_address='00:a0:50:67:55:45', manager=manager)
device.connect()

manager.run()
