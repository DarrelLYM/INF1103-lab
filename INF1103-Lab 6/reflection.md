# INF1103 Lab 6 – Reflection Questions

**1. What is the difference between a class and an object?**
A class is a blueprint that defines what attributes and methods something will have (e.g. `Product`). An object is a specific instance created from that blueprint with its own values, e.g. `Product("P001", "Laptop", 1200.00, 15)`. One class can create many objects.

**2. Why is Product a suitable class for this system?**
Product is the main "noun" in the inventory system. Every product has the same set of data (ID, name, price, stock) and the same behaviours (update stock, display itself), so it makes sense to group that data and behaviour together into one class instead of using loose dictionaries.

**3. What data belongs inside a Product object?**
Its product ID, name, price and stock quantity (`__product_id`, `__name`, `__price`, `__stock`).

**4. Why should the Product class manage its own stock rather than the main program directly changing it?**
If stock is only changed through `update_stock()`, the Product can validate the value (e.g. reject negative stock) in one place. If the main program changed the value directly, every part of the code that changes stock would need its own checks, and a mistake anywhere could leave the product in an invalid state.

**5. What does encapsulation mean in your program?**
Each class keeps its data private (double-underscore attributes such as `__stock` and `__products`) and only exposes public methods to work with it. The main program uses `get_stock()` / `update_stock()` on Product and `add_product()` / `search_product()` / `display_all()` on Inventory, rather than reaching into their internal data. `Inventory.get_all_products()` also returns a copy of the list so outside code cannot change the internal list.

**6. What is the responsibility of the Product class?**
To represent and manage a single product: store its information and control changes to its own state (stock).

**7. What is the responsibility of the Inventory class?**
To manage a collection of Product objects: store them, add new ones (preventing duplicate IDs), search for a product by ID, and display all products.

**8. How does separating these responsibilities demonstrate the Single Responsibility Principle?**
Each class has one reason to change. Product only changes if the definition of a product changes; Inventory only changes if the way products are stored or searched changes; FileHandler only changes if the save format changes; and the main program only changes if the menu or user interaction changes. For example, switching from JSON to a database would only require changing FileHandler.

**9. What information does the main program need to know about a Product?**
Only its public interface: how to create one (ID, name, price, stock) and which methods to call – the getters, `update_stock()` and `display_information()`.

**10. What information about the internal implementation of Product does the main program not need to know?**
How the data is stored internally (the private attribute names and types), how stock validation is done, and how the display string is formatted. The internals could change completely and the main program would still work as long as the public methods stay the same.
