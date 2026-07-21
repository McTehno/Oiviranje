package test.java;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.persistence.EntityManager;

import java.sql.SQLException;
import java.sql.Statement;

class AllScenariosJava {

   void sql(HttpServletRequest request, java.sql.Statement statement) throws Exception {
        String id = request.getParameter("id");
        String query = "SELECT * FROM users WHERE id = " + id;
        statement.executeQuery(query);
    }

    void hql(HttpServletRequest request, jakarta.persistence.EntityManager entityManager) {
        String name = request.getParameter("name");
        entityManager.createQuery("FROM User u WHERE u.name = '" + name + "'").getResultList();
    }

    void command(HttpServletRequest request) throws IOException {
        String host = request.getParameter("host");
        Runtime.getRuntime().exec("ping " + host);
    }

    void mongo(HttpServletRequest request, com.mongodb.client.MongoCollection<org.bson.Document> users) {
        String username = request.getParameter("username");
        org.bson.Document filter = new org.bson.Document("username", username).append("$ne", null);
        users.find(filter);
    }
}
