-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: ecom20
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admindata`
--

DROP TABLE IF EXISTS `admindata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admindata` (
  `adminid` binary(16) NOT NULL,
  `adminname` varchar(50) NOT NULL,
  `adminemail` varchar(100) NOT NULL,
  `address` text,
  `admin_phno` bigint DEFAULT NULL,
  `password` varbinary(255) NOT NULL,
  `agree` enum('on','off') DEFAULT NULL,
  `admin_profileimg` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`adminid`),
  UNIQUE KEY `adminemail` (`adminemail`),
  CONSTRAINT `admindata_chk_1` CHECK ((length(`admin_phno`) = 10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admindata`
--

LOCK TABLES `admindata` WRITE;
/*!40000 ALTER TABLE `admindata` DISABLE KEYS */;
INSERT INTO `admindata` VALUES (_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','Manoj Kumar','bathulamanojkumar11@gmail.com','Guntur',1234567890,_binary '$2b$12$6.911GulQk9CMn1qhgbBGuS2qEH1eg69TWSRzOArSR73NYwhsI6Ki','on','X1oL1i.jpg');
/*!40000 ALTER TABLE `admindata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `itemid` binary(16) NOT NULL,
  `item_name` longtext NOT NULL,
  `item_description` longtext,
  `item_about` longtext,
  `price` decimal(10,2) NOT NULL,
  `quantity` bigint DEFAULT NULL,
  `item_category` enum('home_appliences','grocery','electronics','fashion','toys','sports') DEFAULT NULL,
  `item_imgname` varchar(20) NOT NULL,
  `added_by` binary(16) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`itemid`),
  UNIQUE KEY `item_imgname` (`item_imgname`),
  KEY `added_by` (`added_by`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`added_by`) REFERENCES `admindata` (`adminid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (_binary '\Î{\Å:\È\ñ¾\î\Ğ9W¥ˆ„','Daniel Hechter Paris Bercy Collection Modern Multi Functional Watch for Men with Square Dial and Silicon Band-DHM1001','Case diameter42 Millimetres\r\nBand colourBrown\r\nBand material typeSilicone\r\nWarranty typeLimited\r\nWatch movement typeQuartz\r\nItem weight250 Grams\r\nCountry of OriginIndia','Modern Square Dial Design: Stylish square-shaped dial gives a bold and contemporary look, perfect for everyday and formal wear.\r\nMulti-Functional Display: Equipped with multiple sub-dials for enhanced functionality and a premium feel.\r\nComfortable Silicone Strap: Durable, lightweight, and skin-friendly silicone band ensures all-day comfort.\r\nQuartz Precision Movement: Reliable and accurate timekeeping for daily use.\r\nWater Resistant Build: Suitable for everyday activities like hand washing and light splashes.',3000.00,1,'fashion','Q3fZ1c.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-04-18 07:13:40'),(_binary '\ÃB\Ë:\÷\ñ¾\î\Ğ9W¥ˆ„','Dell 14, AMD Ryzen AI 5 340 6-core/12-thread Processor, 16GB LPDDR5X, 512GB SSD, FHD+, 14\"/35.56cm, Win 11, MSO\'24, Ice Blue, 1.52 Kg, [Dell 14], 300 Nits IPS, Backlit+FPS Keyboard, AI Powered Laptop','\r\nBrand	Dell\r\nModel Name	DB14255\r\nScreen Size	14 Centimetres\r\nColour	Ice Blue\r\nHard Disk Size	512 GB\r\nCPU Model	Ryzen 5\r\nRAM Memory Installed Size	16 GB\r\nOperating System	Windows 11 Home\r\nSpecial Feature	Backlit Keyboard, Fingerprint Reader, Long Battery Life\r\nGraphics Card Description	Integrated','Processor: Built For AI AMD R5-340 AI (16MB, Up to 4.80GHz, 6 Cores)\r\nRAM: 16GB, LPDDR5X, 7500MT/s & Storage: 512GB SSD\r\nDisplay: 14.0\" FHD+ AG NT 300nits WVA/IPS Display w/ ComfortView Support & Graphics: AMD Radeon Graphics\r\nKeyboard: Backlit Keyboard + Fingerprint Reader\r\nPorts: HDMI 1.4*, (2) USB 3.2 Gen 2 Type-C (DP/PowerDelivery, (1) USB 3.2 Gen 1 Type-A, (1) Global Headset\r\nSoftware: Pre-Loaded Windows 11 Home with Lifetime Validity | MS Office Home and Student 2024 with lifetime validity| McAfee Multi Device Security 15-month subscription',80000.00,100,'electronics','Q7aX5i.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-04-18 12:50:08'),(_binary 'D\Ù~ˆa\ñ˜§\Ğ9W¥ˆ„','Skechers Men Summits Brisbane Sneakers','Material typeMesh, Ethylene Vinyl Acetate\r\nClosure typeLace-Up\r\nHeel typeNo Heel\r\nWater resistance levelNot Water Resistant\r\nSole materialEthylene Vinyl Acetate\r\nStyleSneaker\r\nCountry of OriginIndia','About this item\r\nEngineered Knit Lace-Up Sneaker W/ Memory Foam\r\nMEDIUM CUSHIONING',2345.00,200,'sports','Q5fC6f.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-03-05 12:32:27'),(_binary 'F\ÙG—:ı\ñ¾\î\Ğ9W¥ˆ„','Arrow Men Blazer','Material composition| Shell: 74% Polyester, 21% Rayon, 5% Spandex | Lining: 100% Polyester | Dry clean\r\nStyleSingle breasted\r\nClosure typeButton\r\nPatternSolid\r\nCountry of OriginIndia','Premium Quality â€“ Our Arrow blazer for men formal and casual is meticulously crafted from a high-quality fabric with a refined, smooth texture that exudes sophistication. Its breathable construction ensures exceptional comfort and a cool, effortless feel throughout the day.\r\nFit & Design â€“ Our slim fit blazers features design with a notch lapel collar, long sleeves, double-vented back hem and three pockets provides a sharp, structured and contemporary silhouette tailored for a distinguished appearance.\r\nEasy to Pair â€“ Our blazer for men casual & formal pairs with trousers, chinos or jeans elevating every ensemble with refined elegance. This navy blue blazer has versatile design delivering a polished, sophisticated presence ideal for formal events, business meetings or casual wear.\r\nDurable & Long-lasting â€“ Arrow blazer for man has a blend of premium fabrics and is expertly tailored to maintain its structure, color depth and luxurious texture over time. To preserve its impeccable fit and premium finish, it is recommended to dry clean only.\r\nTrusted Brand & Heritage â€“ From the renowned Arrow brand, our men blazer embody authentic style, craftsmanship and quality. Designed with a perfect blend of sophistication these slim fit blazer for men represent enduring elegance and premium tailoring for men who value timeless refinement.',6000.00,5,'fashion','G4wD8n.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-04-18 13:34:51'),(_binary 'IO,:\÷\ñ¾\î\Ğ9W¥ˆ„','SG Economy Cricket Kit, Size 6','\r\nSize	6\r\nColour	Multicolor\r\nMaterial	Nylon, Polyester\r\nSport	Cricket\r\nBrand	SG','SG cricket RSD xtreme Kashmir willow bat\r\nSG cricket helmet\r\nSG cricket batting gloves\r\nSG cricket test thigh pads\r\nSG ball\r\nIn-Box Contents: 1 Cricket Kit Bag, 1 SG Cricket RSD Spark Kasmir Willow Bat Size-6 , 1 Cricket Helmet, 1 Pair Batting Pads, 1 Pair Thigh Pads, 1 Pair Batting Gloves, 1 Abdominal Guard and Cricket Ball',9000.00,7,'sports','H2tK9c.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-04-18 12:51:58'),(_binary '‹cš:\÷\ñ¾\î\Ğ9W¥ˆ„','XM MRP Academy Neo VK-18 Legend Complete Cricket Kit with Genius Bat, Pads, Gloves, Helmet, Bag, Red and White, Professional Set (6 NO (Ideal for 11-14 Years))','COMPLETE KIT: Professional cricket set including XM Genius bat, protective pads, gloves, helmet, and a stylish VK-18 Legend kit bag in red and white colour scheme\r\nPREMIUM BAT: XM Genius cricket bat crafted for optimal performance, perfect for professional and serious players seeking excellence in their game\r\nPROTECTIVE GEAR: High-quality pads and gloves designed with superior padding and comfortable fit, along with a sturdy helmet featuring protective grille\r\nSTORAGE SOLUTION: Spacious VK-18 Legend kit bag with multiple compartments for organised storage of all cricket equipment and accessories\r\nPROFESSIONAL QUALITY: Premium XM Academy Neo series equipment suitable for competitive cricket, designed for durability and performance','Manufacturer	RK SONS ENTERPRISES\r\nPacker	RK SONS ENTERPRISES\r\nItem Weight	5000 kg\r\nItem Dimensions LxWxH	65 x 33 x 15 Centimeters\r\nNet Quantity	9.0 Piece\r\nIncluded Components	YES\r\nGeneric Name	CRICKET KIT\r\nBest Sellers Rank	\r\n#3,332 in Sports, Fitness & Outdoors (See Top 100 in Sports, Fitness & Outdoors)\r\n#46 in Cricket Kits',9000.00,5,'sports','G6rK1a.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-04-18 12:53:48'),(_binary '\ÏÀ:\ö\ñ¾\î\Ğ9W¥ˆ„','ASUS Vivobook 15,13th Gen,Intel Core i7-13620H(Intel UHD iGPU/16GB RAM/1TB SSD/FHD/15.6\"/60Hz/Backlit Keyboard/42Whr/Windows 11/M365 Basic (1Year)*/Office Home 2024/Quiet Blue/1.7 Kg)X1502VA-BQ1298WS','\r\nBrand	ASUS\r\nModel Name	ASUS Vivobook 15\r\nScreen Size	15.6 Inches\r\nColour	Quiet Blue\r\nHard Disk Size	1 TB\r\nCPU Model	Intel Core i7\r\nRAM Memory Installed Size	16 GB\r\nOperating System	Windows 11 Home\r\nSpecial Feature	45% NTSC color gamut, Anti-glare display, Backlit Keyboard\r\nGraphics Card Description	Integrated','Processor : Intel Core i7-13620H Processor 2.4 GHz (24MB Cache, up to 4.9 GHz, 10 cores, 16 Threads)\r\nDisplay : 15.6-inch, FHD (1920 x 1080) 16:9 aspect ratio, 60Hz refresh rate, 250nits Brightness, 45% NTSC color gamut, Anti-glare display, 82% Screen-to-body ratio| Keyboard : Backlit Chiclet Keyboard with Num-key\r\nGraphics : Intergrated Intel UHD Graphics\r\nã€Software : Microsoft 365 Basic with 100GB Cloud Storage for 1 Year + Office Home 2024 with lifetime validity | Operating System : Windows 11 Homeã€‘',72000.00,200,'electronics','J1lZ9w.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-04-18 12:48:33'),(_binary '\ïì§:ü\ñ¾\î\Ğ9W¥ˆ„','Highlander Men\'s Slim Fit Shirt for Men | Checks Shirt | Long Sleeves | Spread Collar | Casual Shirts | Men Shirts | Shirts for Men','Material composition100% Cotton\r\nFit typeSlim Fit\r\nSleeve typeLong Sleeve\r\nCollar styleCutaway\r\nNeck styleCollared Neck\r\nStyleHLSH011439\r\nCountry of OriginIndia','ğŸ“ğŸ›ï¸ Product Description: The menâ€™s olive green and black checked casual shirt is a stylish and versatile wardrobe staple. Featuring a classic checkered pattern, it offers a modern slim fit that enhances the silhouette. Crafted from breathable fabric, it ensures all-day comfort.\r\nğŸ§¶ğŸ‘• Fabric: A 100% cotton woven fabric is breathable, durable, and soft, making it a comfortable choice for everyday wear.\r\nğŸ‘”âœ‚ï¸ Sleeves: Full sleeves with buttoned cuffs for a polished yet casual look.\r\nğŸ­ğŸ’¼ Occasion: Perfect for casual outings, weekend brunches, or informal gatherings. Pair it with jeans or chinos for an effortlessly stylish ensemble\r\nğŸ§ºğŸ§´Care Instructions: Machine wash in cold water on a gentle cycle to prevent shrinkage and fading. Use a mild detergent and avoid bleach to preserve the fabricâ€™s softness and color. Wash similar colors together and turn the garment inside out to reduce wear on the surface.',700.00,5,'fashion','Q8aK9j.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-04-18 13:32:25'),(_binary 'ù¡\Û`\ñ˜§\Ğ9W¥ˆ„','Spooky Creative Starry Sky Ceramic Mug â€“ Cute 3D Cat Design with Lid & Spoon, Perfect for Office, Breakfast, & Gifts â€“ Available in Blue â€“ 420ml','Brand	Spooky\r\nMaterial	Ceramic\r\nColour	Blue - 420ml\r\nCapacity	420 Milliliters\r\nSpecial Feature	Light Up, Non-Slip\r\nStyle	Cartoon - Cat\r\nRecommended Uses For Product	Home, Office, Hotel and Cafe','About this item\r\nğ”ğ§ğ¢ğªğ®ğ ğŸ‘ğƒ ğ‚ğšğ­ ğƒğğ¬ğ¢ğ ğ§: Add some charm to your daily routine with this adorable, three-dimensional cat-shaped mug. The perfect blend of fun and functionality!\r\nğ‡ğ¢ğ ğ¡-ğğ®ğšğ¥ğ¢ğ­ğ² ğ‚ğğ«ğšğ¦ğ¢ğœ ğŒğšğ­ğğ«ğ¢ğšğ¥: Made from durable ceramics, this mug ensures long-lasting use while keeping your drinks warm. Ideal for hot coffee, tea, or milk.\r\nğ‚ğ¨ğ¦ğ©ğ¥ğğ­ğ ğ’ğğ­: Includes a matching lid to keep your drinks warm, a convenient handle for easy holding, and a spoon for stirring â€“ all in one stylish package.\r\nğğğ«ğŸğğœğ­ ğŸğ¨ğ« ğ†ğ¢ğŸğ­ğ¬: A thoughtful gift for friends, colleagues, or loved ones. Whether it\'s for birthdays, promotions, or just to brighten someone\'s day, this mug makes a unique and delightful gift.\r\nğ€ğ¯ğšğ¢ğ¥ğšğ›ğ¥ğ ğ¢ğ§ ğŸ’ ğ“ğ«ğğ§ğğ² ğ‚ğ¨ğ¥ğ¨ğ«ğ¬: Choose from Blue, Purple, Yellow, or Pink to suit your personality and style. A cute addition to any office desk or home kitchen.',899.00,550,'home_appliences','Z5dJ6i.jpg',_binary 'ŸW·¬`\ñ˜§\Ğ9W¥ˆ„','2026-03-05 12:30:19');
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `order_detailsid` int unsigned NOT NULL AUTO_INCREMENT,
  `orderid` int unsigned NOT NULL,
  `itemid` binary(16) DEFAULT NULL,
  `item_name` longtext,
  `item_price` decimal(10,2) DEFAULT NULL,
  `item_qyt` int DEFAULT NULL,
  `item_category` enum('home_appliences','grocery','fashion','toys','sports') DEFAULT NULL,
  `sub_total` decimal(10,2) DEFAULT NULL,
  `item_imgname` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`order_detailsid`),
  KEY `orderid` (`orderid`),
  KEY `itemid` (`itemid`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`orderid`) REFERENCES `orders` (`orderid`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`itemid`) REFERENCES `items` (`itemid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,_binary 'D\Ù~ˆa\ñ˜§\Ğ9W¥ˆ„','Skechers Men Summits Brisbane Sneakers',2345.00,1,'fashion',2345.00,'Q5fC6f.jpg'),(2,2,_binary 'ù¡\Û`\ñ˜§\Ğ9W¥ˆ„','Spooky Creative Starry Sky Ceramic Mug â€“ Cute 3D Cat Design with Lid & Spoon, Perfect for Office, Breakfast, & Gifts â€“ Available in Blue â€“ 420ml',899.00,1,'home_appliences',899.00,'Z5dJ6i.jpg');
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `orderid` int unsigned NOT NULL AUTO_INCREMENT,
  `razorpay_ordid` varchar(100) NOT NULL,
  `razorpay_paymentid` varchar(100) NOT NULL,
  `user_id` binary(16) DEFAULT NULL,
  `grand_total` decimal(10,2) DEFAULT NULL,
  `tax` int DEFAULT NULL,
  `delivery` int DEFAULT NULL,
  `sub_total` decimal(10,2) DEFAULT NULL,
  `status` enum('paid','unpaid') DEFAULT 'paid',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`orderid`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `userdata` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'order_SR4xCEZlgeJiCG','pay_SR4xnk40NwKM5f',_binary '¨%\ÑLa\ñ˜§\Ğ9W¥ˆ„',2502.25,117,40,2345.00,'paid','2026-03-14 16:21:44'),(2,'order_SUaa16EHAU2zaB','pay_SUaaQUrgAQ9vEW',_binary '¨%\ÑLa\ñ˜§\Ğ9W¥ˆ„',983.95,45,40,899.00,'paid','2026-03-23 13:14:49');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `reviewid` int unsigned NOT NULL AUTO_INCREMENT,
  `reviewtext` longtext,
  `rating` enum('1','2','3','4','5') DEFAULT NULL,
  `itemid` binary(16) DEFAULT NULL,
  `userid` binary(16) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reviewid`),
  KEY `itemid` (`itemid`),
  KEY `userid` (`userid`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`itemid`) REFERENCES `items` (`itemid`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `userdata` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdata`
--

DROP TABLE IF EXISTS `userdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdata` (
  `userid` binary(16) NOT NULL,
  `username` varchar(50) NOT NULL,
  `useremail` varchar(50) NOT NULL,
  `user_phno` varchar(20) DEFAULT NULL,
  `user_address` tinytext,
  `user_password` varbinary(255) NOT NULL,
  `user_gender` enum('male','female','others') DEFAULT NULL,
  `user_agree` enum('on','off') DEFAULT 'on',
  PRIMARY KEY (`userid`),
  UNIQUE KEY `useremail` (`useremail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdata`
--

LOCK TABLES `userdata` WRITE;
/*!40000 ALTER TABLE `userdata` DISABLE KEYS */;
INSERT INTO `userdata` VALUES (_binary '¨%\ÑLa\ñ˜§\Ğ9W¥ˆ„','Manoj Kumar Bathula','bathulamanojkumar11@gmail.com','9177310453','Guntur',_binary '$2b$12$RZxjv.UmuFDxgaDgax.CTu3sJRp6XDIEHCkYlRhPJTauR6o31q43C','male','on');
/*!40000 ALTER TABLE `userdata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-27 14:56:23
