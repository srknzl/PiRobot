package com.srknzl.PiRobot;


import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;

import java.util.Set;

public class Bluetooth {
    public static BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    public static boolean connected = false;
    /*
    Desc: Queries paired devices and connects to name raspberrypi if it exists in paired devices

     */
    public static boolean connectIfPaired(Context c){
        Set<BluetoothDevice> pairedDevices = bluetoothAdapter.getBondedDevices();

        if (pairedDevices.size() > 0) {
            // There are paired devices. Get the name and address of each paired device.
            for (BluetoothDevice device : pairedDevices) {
                String deviceName = device.getName();
                String deviceHardwareAddress = device.getAddress(); // MAC address
                if(deviceName.equals("raspberrypi")){

                    ConnectThread connectThread = new ConnectThread(device, c);
                    connectThread.start();
                    try {
                        connectThread.join();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                        return false;
                    }
                }
            }
        }
        return connected;
    }
}
