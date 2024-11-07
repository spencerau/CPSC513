// 1. Write a query to return any pair of two users who have a shared interest but are not yet currently friends.
MATCH (user1:User)-[:INTERESTED_IN]->(i:Interest)<-[:INTERESTED_IN]-(user2:User)
WHERE id(user1) < id(user2) AND  
    NOT (EXISTS((user1)-[:FRIENDS_WITH]-(user2)) OR 
    EXISTS((user2)-[:FRIENDS_WITH]-(user1)))
RETURN user1.name AS User1, user2.name AS User2, i.name AS Shared_Interest


// 2. Write a query to return the names of all friends-of-friends that are NOT friends with the user John.
// user1 is friends with John, user2 is friends with user1, user2 is NOT friends with John
MATCH (john:User {name: 'John'})-[:FRIENDS_WITH]->(user1:User)<-[:FRIENDS_WITH]-(user2:User)
WHERE id(user1) < id(user2) AND
    NOT (EXISTS((john)-[:FRIENDS_WITH]-(user2)) OR 
    EXISTS((user2)-[:FRIENDS_WITH]-(john)))
RETURN user2.name AS User2, user1.name AS Friend_of_John


// 3. Write a query to return pairs of users, and how many shared interests these two users have.
MATCH (user1:User)-[:INTERESTED_IN]->(i:Interest)<-[:INTERESTED_IN]-(user2:User)
WHERE id(user1) < id(user2)
RETURN user1.name AS User1, user2.name AS User2, COUNT(i)AS Num_Shared_Interest


// 4. Create a query, based on the logic of the queries from questions 1 and 2, to identify all
// users who have a shared interest but are not friends. Identify if these two users have any
// friends in common. If they do, within that same query, add these users as friends of each
// other with a new relationship.
MATCH (user1:User)-[:INTERESTED_IN]->(i:Interest)<-[:INTERESTED_IN]-(user2:User)
WHERE id(user1) < id(user2) AND  
    NOT (EXISTS((user1)-[:FRIENDS_WITH]-(user2)) OR 
    EXISTS((user2)-[:FRIENDS_WITH]-(user1)))
WITH user1, user2
MATCH 
    (user1)-[:FRIENDS_WITH]->(commonFriend:User)<-[:FRIENDS_WITH]-(user2)
CREATE 
    (user1)-[:FRIENDS_WITH]->(user2)
    (user2)-[:FRIENDS_WITH]->(user1)
RETURN user1.name AS User1, user2.name AS User2, commonFriend.name AS Common_Friend

