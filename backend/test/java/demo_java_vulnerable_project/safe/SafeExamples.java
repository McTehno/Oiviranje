package test.java.demo_java_vulnerable_project.safe;

public class SafeExamples {
    public void safeSql(java.sql.PreparedStatement statement, String id) throws Exception {
        statement.setString(1, id);
        statement.executeQuery();
    }
}
package test.java.demo_java_vulnerable_project.safe;

import com.mongodb.client.MongoCollection;
import jakarta.persistence.EntityManager;
import jakarta.servlet.http.HttpServletRequest;
import org.bson.Document;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class SafeExamples {

    // 1. Varna parametrizirana SQL-poizvedba
    public void safeFindUser(
        HttpServletRequest request,
        Connection connection
    ) throws Exception {
        String userId =
            request.getParameter("id");

        String sql =
            "SELECT * FROM users WHERE id = ?";

        try (
            PreparedStatement statement =
                connection.prepareStatement(sql)
        ) {
            statement.setString(1, userId);

            try (ResultSet result = statement.executeQuery()) {
                // Obdelava rezultata
            }
        }
    }


    // 2. Varna SQL-posodobitev
    public void safeUpdateOrder(
        HttpServletRequest request,
        Connection connection
    ) throws Exception {
        String orderId =
            request.getParameter("order_id");

        String status =
            request.getParameter("status");

        String sql =
            "UPDATE orders SET status = ? WHERE id = ?";

        try (
            PreparedStatement statement =
                connection.prepareStatement(sql)
        ) {
            statement.setString(1, status);
            statement.setString(2, orderId);
            statement.executeUpdate();
        }
    }


    // 3. Varna parametrizirana HQL-poizvedba
    public void safeHqlQuery(
        HttpServletRequest request,
        EntityManager entityManager
    ) {
        String role =
            request.getParameter("role");

        entityManager
            .createQuery(
                "FROM User u WHERE u.role = :role"
            )
            .setParameter("role", role)
            .getResultList();
    }


    // 4. Statičen ukaz brez uporabniškega vnosa
    public String safeStaticCommand() {
        return "echo backup started";
    }


    // 5. Fiksen program z ločenim argumentom
    public void saferPing(
        HttpServletRequest request
    ) throws Exception {
        String host =
            request.getParameter("host");

        if (
            host == null
                || !host.matches("[A-Za-z0-9.-]+")
        ) {
            throw new IllegalArgumentException(
                "Invalid host"
            );
        }

        new ProcessBuilder(
            "ping",
            "-c",
            "1",
            host
        ).start();
    }


    // 6. MongoDB poizvedba s fiksnim poljem
    public void safeFindMongoUser(
        HttpServletRequest request,
        MongoCollection<Document> users
    ) {
        String username =
            request.getParameter("username");

        if (
            username == null
                || !username.matches("[A-Za-z0-9_.-]+")
        ) {
            throw new IllegalArgumentException(
                "Invalid username"
            );
        }

        Document query =
            new Document("username", username);

        users.find(query);
    }
}