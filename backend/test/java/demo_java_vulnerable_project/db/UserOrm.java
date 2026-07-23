/*package test.java.demo_java_vulnerable_project.db;
import jakarta.servlet.http.HttpServletRequest;
public class UserOrm {
    public void find(HttpServletRequest request, jakarta.persistence.EntityManager entityManager) {
        String role = request.getParameter("role");
        entityManager.createQuery("FROM User u WHERE u.role = '" + role + "'").getResultList();
    }
}
*/
package test.java.demo_java_vulnerable_project.db;

import jakarta.persistence.EntityManager;
import jakarta.servlet.http.HttpServletRequest;

public class UserOrm {

    // 1. HQL Injection s konkatenacijo
    public void findUserByRole(HttpServletRequest request,EntityManager entityManager) {
        String role = request.getParameter("role");

        String hql ="FROM User u WHERE u.role = '" + role + "'";

        entityManager.createQuery(hql).getResultList();
    }


    // 2. HQL Injection z uporabniškim imenom
    public void findUserByUsername(HttpServletRequest request,EntityManager entityManager) {
        String username = request.getParameter("username");

        String hql = String.format("FROM User u WHERE u.username = '%s'",username);

        entityManager.createQuery(hql).getResultList();
    }


    // 3. HQL Injection v pogoju LIKE
    public void searchUsers(HttpServletRequest request,EntityManager entityManager) {
        String search = request.getParameter("search");

        String hql ="FROM User u WHERE u.username LIKE '%"+ search + "%'";

        entityManager.createQuery(hql).getResultList();
    }


    // 4. Neposreden uporabniški vhod v createQuery()
    public void findUserDirectly(HttpServletRequest request,EntityManager entityManager) {
        entityManager.createQuery("FROM User u WHERE u.id = "+ request.getParameter("id")).getResultList();
    }
}
