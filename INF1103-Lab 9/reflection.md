lab 9 reflection

predict first answers + 1.5 diagnose are in the Lab 9 Predict First Notes doc

what I changed from lab 8
- discount_strategy.py - DiscountStrategy (abstract, apply(total)) + NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
- Order gets a strategy when it's made (NoDiscount() if none), set_discount() to swap it, calculate_total() just calls apply(). no if/elif for discounts in Order
- product_factory.py - ProductFactory.create() returns a Product. menu, FileHandler and the csv loader all use it now, only the factory calls PhysicalProduct/DigitalProduct. unknown type -> ValueError
- validation: price > 0 and stock >= 0 in Product, quantity > 0 in OrderLine. each class checks its own stuff
- input_helpers.py - get_positive_float, get_non_negative_int, get_positive_int, keep asking until valid
- product_loader.py - load_products() with try/except/else/finally, reads products.csv, bad rows get skipped. also menu option 10
- broken inventory.json starts fresh instead of crashing, and save failing (OSError) just prints a message
- UML has DiscountStrategy + the 4 subclasses, Order 0..* -> 1 DiscountStrategy, and ProductFactory with a dashed <<creates>> arrow to Product

testing
python lab9_demo.py for the predict first stuff
python -m unittest discover -s tests -v -> 56 tests (21 old lab 8 ones + 35 new). no input or internet needed so it could run in CI
all the excepts catch a specific exception (ValueError, FileNotFoundError, KeyError, JSONDecodeError, OSError), there's a test that checks for bare except / except Exception

section 8

pattern making it more complicated - the main menu. it's a long if/elif but each option just calls a function and the options never change, making a class per option would be way too much. same with Supplier, only one kind so a factory would just wrap the constructor

factory moving the OCP problem - think it's worth it here. before there were 3 places with their own if/else for product types, now just 1. still have to edit create() for a new type but it's one small method. a registry would get rid of the if/elif but with only 2 types it's more code than it saves

rejecting the whole file vs skipping rows - if the rows depend on each other or half loading would be misleading. like a stock take file that replaces the whole inventory, or a price update where some products get new prices and some don't. then I'd check every row first and only add if all are ok

validation vs exception - validation is my own rule with an if, e.g. if quantity <= 0: raise ValueError in OrderLine. exception is python failing to do something, e.g. float("abc") -> ValueError or open() -> FileNotFoundError in load_products(). my validation also raises ValueError so one except ValueError catches both (get_positive_float and the csv loader do this)

predictions that didn't match - 3 were close but not exact. 5.1 I thought it'd return 12.50 but it's 12.5, decimals only show when formatting. 5.2 I thought the abc price would fail my price > 0 check but float("abc") failed first in Product.__init__ so it's python's message. 3.3 forgot the menu also lists the product types so it needs a new entry too

group project
- exporters/ already uses a factory, ExporterFactory.create(name) gives back an IncidentExporter (csv or json) so the export code only uses the base type. same idea as ProductFactory
- the enrichment steps in ai_manager.py are kind of strategy. EnrichmentStep is abstract with run(), HazardFlagStep and ReviewStep implement it and they all get called through safe_run() the same way, so the weather/web search steps are just new classes not new branches
- a factory for the AI clients would be over engineering for now since we only use one Gemini client and it gets passed into the steps. if we had to switch between providers at runtime then maybe
