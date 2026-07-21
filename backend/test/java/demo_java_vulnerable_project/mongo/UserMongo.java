package test.java.demo_java_vulnerable_project.mongo;

import jakarta.servlet.http.HttpServletRequest;

public class UserMongo {
     public void find(HttpServletRequest request, com.mongodb.client.MongoCollection<org.bson.Document> users) {
        String username = request.getParameter("username");
        org.bson.Document filter = new org.bson.Document("username", username).append("$ne", null);
        users.find(filter);
    }
}
