/*package test.java.demo_java_vulnerable_project;

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
*/
package test.java.demo_java_vulnerable_project;

import test.java.demo_java_vulnerable_project.db.UserOrm;
import test.java.demo_java_vulnerable_project.db.UserSQL;
import test.java.demo_java_vulnerable_project.mongo.UserMongo;
import test.java.demo_java_vulnerable_project.system.CommandTools;

import jakarta.persistence.EntityManager;
import jakarta.servlet.http.HttpServletRequest;

import com.mongodb.client.MongoCollection;
import org.bson.Document;

import java.sql.Statement;

public class App {

    public void run(
        HttpServletRequest request,
        Statement statement,
        EntityManager entityManager,
        MongoCollection<Document> users
    ) throws Exception {

        UserSQL userSQL = new UserSQL();
        userSQL.findUserById(request, statement);
        userSQL.findUserByEmail(request, statement);

        UserOrm userOrm = new UserOrm();
        userOrm.findUserByRole(request, entityManager);

        CommandTools commandTools = new CommandTools();
        commandTools.pingHost(request);
        commandTools.showFile(request);

        UserMongo userMongo = new UserMongo();
        userMongo.findMongoUser(request, users);
        userMongo.deleteMongoUser(request, users);
    }
}