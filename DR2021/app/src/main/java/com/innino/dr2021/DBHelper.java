package com.innino.dr2021;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.provider.BaseColumns;

import java.util.List;

final class DBHelperName {
    private DBHelperName() {}

    public static class Names implements BaseColumns{
        public static final String TABLE_NAME = "history";
        public static final String ID_PERSON = "id";
        public static final String VD = "vd";
        public static final String ND = "nd";
        public static final String BPM = "bpm";
        public static final String TIME = "time";
    }
}

public class DBHelper extends SQLiteOpenHelper {
    private static final String SQL_CREATE_ENTRIES =
            "CREATE TABLE " + DBHelperName.Names.TABLE_NAME + " (" +
                    DBHelperName.Names._ID + " INTEGER PRIMARY KEY," +
                    DBHelperName.Names.ID_PERSON + " TEXT," +
                    DBHelperName.Names.VD + " TEXT," +
                    DBHelperName.Names.ND + " TEXT," +
                    DBHelperName.Names.BPM + " TEXT," +
                    DBHelperName.Names.TIME + " TEXT)";
    private static final String SQL_DELETE_ENTRIES =
            "DROP TABLE IF EXISTS " + DBHelperName.Names.TABLE_NAME;
    // If you change the database schema, you must increment the database version.
    public static final int DATABASE_VERSION = 2;
    public static final String DATABASE_NAME = "FeedReader.db";

    public DBHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(SQL_CREATE_ENTRIES);
    }
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // This database is only a cache for online data, so its upgrade policy is
        // to simply to discard the data and start over
        db.execSQL(SQL_DELETE_ENTRIES);
        onCreate(db);
    }
    public void onDowngrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        onUpgrade(db, oldVersion, newVersion);
    }

    public boolean InsertEntties(HistoryEntitle obj) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues cv = new ContentValues();
        cv.put(DBHelperName.Names.ID_PERSON, "0");
        cv.put(DBHelperName.Names.VD, obj.td);
        cv.put(DBHelperName.Names.ND, obj.dd);
        cv.put(DBHelperName.Names.BPM, obj.bpm);
        cv.put(DBHelperName.Names.TIME, obj.time);
        long result = db.insert(DBHelperName.Names.TABLE_NAME, null, cv);
        if (result == -1)
            return false;
        else
            return true;
    }
}