package com.srknzl.PiRobot;

public class Model {
    String title;
    String desc;
    int icon;

    //constructor
    public Model(String title, String desc, int icon) {
        this.title = title;
        this.desc = desc;
        this.icon = icon;
    }
    //cons2
    public Model(String title) {
        this.title = title;
    }

    //getters


    public String getTitle() {
        return this.title;
    }

    public String getDesc() {
        return this.desc;
    }

    public int getIcon() {
        return this.icon;
    }
}