import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import { Phone, Mail, MapPin, Clock, Star, Utensils, ChefHat, Truck } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Menu Category Component
const MenuCategory = ({ category, items, categoryNames }) => (
  <div className="mb-12">
    <h3 className="text-2xl font-bold text-orange-600 mb-6 border-b-2 border-orange-200 pb-2">
      {categoryNames[category]}
    </h3>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {items.map((item) => (
        <div key={item.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex justify-between items-start mb-3">
            <div className="flex-1">
              <h4 className="text-lg font-semibold text-gray-800 mb-2 flex items-center">
                {item.name}
                {item.is_spicy && <span className="ml-2 text-red-500">🌶️</span>}
              </h4>
              <p className="text-gray-600 text-sm mb-3 line-clamp-2">{item.description}</p>
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <Clock className="w-4 h-4 mr-1" />
                <span>{item.preparation_time} mins</span>
              </div>
            </div>
            <div className="text-right ml-4">
              <div className="text-xl font-bold text-orange-600">₹{item.price}</div>
              {!item.is_available && (
                <span className="text-red-500 text-sm">Out of Stock</span>
              )}
            </div>
          </div>
          <div className="flex flex-wrap gap-1">
            {item.ingredients.slice(0, 4).map((ingredient, idx) => (
              <span key={idx} className="bg-orange-50 text-orange-700 px-2 py-1 rounded-full text-xs">
                {ingredient}
              </span>
            ))}
            {item.ingredients.length > 4 && (
              <span className="text-gray-500 text-xs">+{item.ingredients.length - 4} more</span>
            )}
          </div>
        </div>
      ))}
    </div>
  </div>
);

// Restaurant Header Component
const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <Utensils className="w-8 h-8 text-orange-600 mr-3" />
            <h1 className="text-2xl font-bold text-gray-800">Shriyansh Restaurant</h1>
          </div>
          <nav className="hidden md:flex space-x-6">
            <a href="#home" className="text-gray-700 hover:text-orange-600 transition-colors">Home</a>
            <a href="#menu" className="text-gray-700 hover:text-orange-600 transition-colors">Menu</a>
            <a href="#about" className="text-gray-700 hover:text-orange-600 transition-colors">About</a>
            <a href="#contact" className="text-gray-700 hover:text-orange-600 transition-colors">Contact</a>
          </nav>
          <button
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <div className="w-6 h-6 flex flex-col justify-center items-center">
              <span className={`bg-gray-800 block transition-all duration-300 ease-out h-0.5 w-6 rounded-sm ${isMenuOpen ? 'rotate-45 translate-y-1' : '-translate-y-0.5'}`}></span>
              <span className={`bg-gray-800 block transition-all duration-300 ease-out h-0.5 w-6 rounded-sm my-0.5 ${isMenuOpen ? 'opacity-0' : 'opacity-100'}`}></span>
              <span className={`bg-gray-800 block transition-all duration-300 ease-out h-0.5 w-6 rounded-sm ${isMenuOpen ? '-rotate-45 -translate-y-1' : 'translate-y-0.5'}`}></span>
            </div>
          </button>
        </div>
        {isMenuOpen && (
          <nav className="md:hidden mt-4 pb-4">
            <a href="#home" className="block py-2 text-gray-700 hover:text-orange-600">Home</a>
            <a href="#menu" className="block py-2 text-gray-700 hover:text-orange-600">Menu</a>
            <a href="#about" className="block py-2 text-gray-700 hover:text-orange-600">About</a>
            <a href="#contact" className="block py-2 text-gray-700 hover:text-orange-600">Contact</a>
          </nav>
        )}
      </div>
    </header>
  );
};

// Hero Section Component
const HeroSection = () => (
  <section id="home" className="relative bg-gradient-to-r from-orange-500 to-red-500 text-white py-20">
    <div className="absolute inset-0 bg-black opacity-50"></div>
    <div className="relative container mx-auto px-4 text-center">
      <h1 className="text-5xl md:text-6xl font-bold mb-6">
        Welcome to <span className="text-yellow-300">Shriyansh Restaurant</span>
      </h1>
      <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
        Authentic Pure Vegetarian Indian Cuisine in the Heart of Narsinghpur, Madhya Pradesh
      </p>
      <div className="flex flex-col md:flex-row gap-4 justify-center items-center mb-8">
        <div className="flex items-center bg-white bg-opacity-20 px-4 py-2 rounded-full">
          <Star className="w-5 h-5 text-yellow-300 mr-2" />
          <span>100% Pure Vegetarian</span>
        </div>
        <div className="flex items-center bg-white bg-opacity-20 px-4 py-2 rounded-full">
          <ChefHat className="w-5 h-5 text-yellow-300 mr-2" />
          <span>Traditional Recipes</span>
        </div>
        <div className="flex items-center bg-white bg-opacity-20 px-4 py-2 rounded-full">
          <Truck className="w-5 h-5 text-yellow-300 mr-2" />
          <span>Takeout • Delivery • Catering</span>
        </div>
      </div>
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="#menu" className="bg-yellow-500 hover:bg-yellow-600 text-black px-8 py-3 rounded-full font-semibold transition-colors">
          View Our Menu
        </a>
        <a href="tel:+91-XXXXXXXXXX" className="bg-transparent border-2 border-white hover:bg-white hover:text-orange-600 px-8 py-3 rounded-full font-semibold transition-colors">
          Order Now
        </a>
      </div>
    </div>
  </section>
);

// About Section Component
const AboutSection = () => (
  <section id="about" className="py-16 bg-gray-50">
    <div className="container mx-auto px-4">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-4">About Shriyansh Restaurant</h2>
        <div className="w-24 h-1 bg-orange-500 mx-auto mb-6"></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <div>
          <img 
            src="https://images.unsplash.com/photo-1620395458832-6436796c2d4c" 
            alt="Restaurant Interior" 
            className="rounded-lg shadow-lg w-full h-96 object-cover"
          />
        </div>
        <div>
          <h3 className="text-3xl font-bold text-gray-800 mb-6">Pure Vegetarian Excellence</h3>
          <p className="text-gray-600 mb-6 leading-relaxed">
            Located in the beautiful city of Narsinghpur, Madhya Pradesh, Shriyansh Restaurant has been serving 
            authentic pure vegetarian Indian cuisine with passion and dedication. Our commitment to quality, 
            traditional recipes, and exceptional service has made us a favorite among locals, tourists, families, 
            and business professionals alike.
          </p>
          <p className="text-gray-600 mb-6 leading-relaxed">
            We specialize in North Indian cuisine and regional specialties, using only the freshest ingredients 
            and time-honored cooking techniques. Every dish is prepared with love and attention to detail, 
            ensuring an unforgettable dining experience.
          </p>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 bg-white rounded-lg shadow">
              <Utensils className="w-8 h-8 text-orange-600 mx-auto mb-2" />
              <h4 className="font-semibold text-gray-800">Takeout</h4>
            </div>
            <div className="text-center p-4 bg-white rounded-lg shadow">
              <Truck className="w-8 h-8 text-orange-600 mx-auto mb-2" />
              <h4 className="font-semibold text-gray-800">Delivery</h4>
            </div>
            <div className="text-center p-4 bg-white rounded-lg shadow">
              <ChefHat className="w-8 h-8 text-orange-600 mx-auto mb-2" />
              <h4 className="font-semibold text-gray-800">Catering</h4>
            </div>
            <div className="text-center p-4 bg-white rounded-lg shadow">
              <Star className="w-8 h-8 text-orange-600 mx-auto mb-2" />
              <h4 className="font-semibold text-gray-800">Quality</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
);

// Contact Section Component
const ContactSection = () => (
  <section id="contact" className="py-16 bg-gray-800 text-white">
    <div className="container mx-auto px-4">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold mb-4">Contact Us</h2>
        <div className="w-24 h-1 bg-orange-500 mx-auto mb-6"></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="text-center">
          <MapPin className="w-12 h-12 text-orange-500 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">Location</h3>
          <p className="text-gray-300">Narsinghpur</p>
          <p className="text-gray-300">Madhya Pradesh, India</p>
        </div>
        <div className="text-center">
          <Phone className="w-12 h-12 text-orange-500 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">Phone</h3>
          <p className="text-gray-300">+91-XXXXXXXXXX</p>
          <p className="text-sm text-gray-400 mt-2">Call for orders & reservations</p>
        </div>
        <div className="text-center">
          <Clock className="w-12 h-12 text-orange-500 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">Hours</h3>
          <p className="text-gray-300">Mon-Fri: 11:00 AM - 10:00 PM</p>
          <p className="text-gray-300">Sat-Sun: 11:00 AM - 11:00 PM</p>
        </div>
      </div>
      <div className="text-center mt-12">
        <Mail className="w-8 h-8 text-orange-500 mx-auto mb-2" />
        <p className="text-gray-300">info@shriyanshrestaurant.com</p>
      </div>
    </div>
  </section>
);

// Footer Component
const Footer = () => (
  <footer className="bg-gray-900 text-white py-8">
    <div className="container mx-auto px-4 text-center">
      <div className="flex items-center justify-center mb-4">
        <Utensils className="w-6 h-6 text-orange-500 mr-2" />
        <span className="text-xl font-bold">Shriyansh Restaurant</span>
      </div>
      <p className="text-gray-400 mb-4">Authentic Pure Vegetarian Indian Cuisine</p>
      <p className="text-gray-500 text-sm">
        © 2025 Shriyansh Restaurant. All rights reserved. | Narsinghpur, Madhya Pradesh
      </p>
    </div>
  </footer>
);

// Main Home Component
const Home = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [restaurantInfo, setRestaurantInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const categoryNames = {
    appetizers: "🥘 Appetizers",
    main_course: "🍛 Main Course", 
    breads: "🍞 Breads",
    rice: "🍚 Rice & Biryani",
    beverages: "🥤 Beverages",
    desserts: "🍮 Desserts",
    snacks: "🍴 Snacks"
  };

  const fetchData = async () => {
    try {
      setLoading(true);
      const [menuResponse, infoResponse] = await Promise.all([
        axios.get(`${API}/menu`),
        axios.get(`${API}/restaurant-info`)
      ]);
      
      setMenuItems(menuResponse.data);
      setRestaurantInfo(infoResponse.data);
      setError(null);
    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to load restaurant data. Please try again later.");
    } finally {
      setLoading(false); 
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading delicious menu...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={fetchData}
            className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Group menu items by category
  const groupedMenu = menuItems.reduce((acc, item) => {
    if (!acc[item.category]) {
      acc[item.category] = [];
    }
    acc[item.category].push(item);
    return acc;
  }, {});

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <HeroSection />
      
      {/* Menu Section */}
      <section id="menu" className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-800 mb-4">Our Menu</h2>
            <div className="w-24 h-1 bg-orange-500 mx-auto mb-6"></div>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Discover our extensive collection of authentic pure vegetarian dishes, 
              each prepared with the finest ingredients and traditional recipes.
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow-lg p-8">
            {Object.entries(groupedMenu).map(([category, items]) => (
              <MenuCategory 
                key={category} 
                category={category} 
                items={items} 
                categoryNames={categoryNames}
              />
            ))}
          </div>

          <div className="text-center mt-12">
            <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-4">Ready to Order?</h3>
              <p className="mb-6">Call us now for takeout, delivery, or catering services!</p>
              <a 
                href="tel:+91-XXXXXXXXXX" 
                className="bg-white text-orange-600 px-8 py-3 rounded-full font-semibold hover:bg-gray-100 transition-colors inline-flex items-center"
              >
                <Phone className="w-5 h-5 mr-2" />
                Call Now: +91-XXXXXXXXXX
              </a>
            </div>
          </div>
        </div>
      </section>

      <AboutSection />
      <ContactSection />
      <Footer />
    </div>
  );
};

// App Component
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
