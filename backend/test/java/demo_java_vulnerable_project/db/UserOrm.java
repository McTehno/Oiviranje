package test.java.demo_java_vulnerable_project.db;
import jakarta.servlet.http.HttpServletRequest;
public class UserOrm {
    public void find(HttpServletRequest request, jakarta.persistence.EntityManager entityManager) {
        String role = request.getParameter("role");
        entityManager.createQuery("FROM User u WHERE u.role = '" + role + "'").getResultList();
    }
}
