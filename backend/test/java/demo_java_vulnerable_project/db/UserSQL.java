package test.java.demo_java_vulnerable_project.db;
import jakarta.servlet.http.HttpServletRequest;
public class UserSQL {
   public void find(HttpServletRequest request, java.sql.Statement statement) throws Exception {
        String id = request.getParameter("id");
        statement.executeQuery("SELECT * FROM users WHERE id = " + id);
    }
}
