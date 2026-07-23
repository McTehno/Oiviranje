/*package test.java.demo_java_vulnerable_project.mongo;

import jakarta.servlet.http.HttpServletRequest;

public class UserMongo {
     public void find(HttpServletRequest request, com.mongodb.client.MongoCollection<org.bson.Document> users) {
        String username = request.getParameter("username");
        org.bson.Document filter = new org.bson.Document("username", username).append("$ne", null);
        users.find(filter);
    }
}*/
package test.java.demo_java_vulnerable_project.mongo;

import com.mongodb.client.MongoCollection;
import jakarta.servlet.http.HttpServletRequest;
import org.bson.Document;

public class UserMongo {

    // 1. Celoten MongoDB filter prihaja od uporabnika
    public void findMongoUser(HttpServletRequest request,MongoCollection<Document> users) {
        String filterJson =request.getParameter("filter");

        Document filter =Document.parse(filterJson);

        users.find(filter);
    }


    // 2. Filter iz uporabniškega vnosa v find()
    public void findMongoUserByBody(HttpServletRequest request,MongoCollection<Document> users) {
        String queryFilter =request.getParameter("query");

        Document filter =Document.parse(queryFilter);

        users.find(filter);
    }


    // 3. Uporabniški vhod kot vrednost operatorja $ne
    public void findWithOperator(HttpServletRequest request,MongoCollection<Document> users) {
        String username =request.getParameter("username");

        Document query = new Document("username",new Document("$ne", username));

        users.find(query);
    }


    // 4. Uporabnik določa ime MongoDB operatorja
    public void findWithDynamicOperator(HttpServletRequest request,MongoCollection<Document> users) {
        String operator =request.getParameter("operator");

        String value =request.getParameter("value");

        Document condition =new Document(operator, value);

        Document query =new Document("enabled", condition);

        users.find(query);
    }


    // 5. Nezaupanja vreden filter pri brisanju
    public void deleteMongoUser(HttpServletRequest request,MongoCollection<Document> users) {
        String filterJson =request.getParameter("filter");

        Document filter =Document.parse(filterJson);

        users.deleteOne(filter);
    }


    // 6. Neposredna uporaba uporabniškega filtra
    public void findMongoUserDirectly(HttpServletRequest request,MongoCollection<Document> users) {
        users.find(Document.parse(request.getParameter("filter")));
    }
}