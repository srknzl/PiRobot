package com.srknzl.PiRobot;


import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;

import java.io.IOException;
import java.util.Set;
import java.util.UUID;

public class Bluetooth {
    public static BluetoothAdapter bluetoothAdapter;


    /*
    Desc: Queries paired devices and connects to name raspberrypi if it exists in paired devices

     */
    public boolean connectIfPaired(){
        Set<BluetoothDevice> pairedDevices = bluetoothAdapter.getBondedDevices();

        if (pairedDevices.size() > 0) {
            // There are paired devices. Get the name and address of each paired device.
            for (BluetoothDevice device : pairedDevices) {
                String deviceName = device.getName();
                String deviceHardwareAddress = device.getAddress(); // MAC address
                if(deviceName.equals("raspberrypi")){

                    try {
                        device.createRfcommSocketToServiceRecord(uuid);
                    } catch (IOException e) {
                        e.printStackTrace();
                        return false;
                    }
                    return true;
                }
            }
        }
    }
}
