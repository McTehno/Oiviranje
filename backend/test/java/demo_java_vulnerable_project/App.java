package test.java.demo_java_vulnerable_project;

import test.java.demo_java_vulnerable_project.db.UserOrm;
import test.java.demo_java_vulnerable_project.db.UserSQL;
import test.java.demo_java_vulnerable_project.mongo.UserMongo;
import test.java.demo_java_vulnerable_project.system.CommandTools;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
public class App {

    public void run(HttpServletRequest request, HttpServletResponse response) throws Exception {
        // SQL Injection
        UserSQL userSQL = new UserSQL();
        userSQL.find(request, null);

        // HQL Injection
        UserOrm userOrm = new UserOrm();
        userOrm.find(request, null);

        // Command Injection
        CommandTools commandTools = new CommandTools();
        commandTools.ping(request);

        // MongoDB Injection
        UserMongo userMongo = new UserMongo();
        userMongo.find(request, null);
    }
    
}
