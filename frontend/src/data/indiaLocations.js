// Reference data: Indian States/UTs mapped to their districts, used for
// cascading State -> District dropdowns on the Farm Profile page.
// This is standard public administrative data (not exhaustive to every
// recent district split, but covers all states/UTs with their major
// districts) -- update as needed for newly created districts.

const INDIA_LOCATIONS = {
  "Maharashtra": [
    "Mumbai City", "Mumbai Suburban", "Thane", "Palghar", "Raigad", "Ratnagiri", "Sindhudurg",
    "Pune", "Satara", "Sangli", "Solapur", "Kolhapur",
    "Nashik", "Dhule", "Nandurbar", "Jalgaon", "Ahmednagar",
    "Aurangabad", "Jalna", "Beed", "Latur", "Osmanabad", "Nanded", "Parbhani", "Hingoli",
    "Amravati", "Akola", "Washim", "Buldhana", "Yavatmal",
    "Nagpur", "Wardha", "Chandrapur", "Gadchiroli", "Gondia", "Bhandara",
  ],
  "Karnataka": [
    "Bengaluru Urban", "Bengaluru Rural", "Mysuru", "Belagavi", "Hubballi-Dharwad", "Mangaluru",
    "Kalaburagi", "Ballari", "Vijayapura", "Shivamogga", "Tumakuru", "Davanagere", "Bidar",
    "Raichur", "Kolar", "Mandya", "Hassan", "Udupi", "Chikkamagaluru", "Kodagu",
  ],
  "Tamil Nadu": [
    "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Erode",
    "Vellore", "Thanjavur", "Dindigul", "Cuddalore", "Kanchipuram", "Thoothukudi", "Nagapattinam",
  ],
  "Andhra Pradesh": [
    "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Kadapa", "Anantapur",
    "Chittoor", "East Godavari", "West Godavari", "Srikakulam", "Prakasam",
  ],
  "Telangana": [
    "Hyderabad", "Rangareddy", "Medchal-Malkajgiri", "Warangal", "Nizamabad", "Karimnagar",
    "Khammam", "Nalgonda", "Adilabad", "Mahbubnagar",
  ],
  "Kerala": [
    "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", "Kottayam", "Idukki",
    "Ernakulam", "Thrissur", "Palakkad", "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod",
  ],
  "Gujarat": [
    "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Junagadh", "Gandhinagar",
    "Anand", "Kutch", "Mehsana", "Navsari", "Valsad",
  ],
  "Rajasthan": [
    "Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Alwar", "Bharatpur", "Sikar",
    "Pali", "Nagaur", "Sri Ganganagar",
  ],
  "Uttar Pradesh": [
    "Lucknow", "Kanpur Nagar", "Varanasi", "Agra", "Meerut", "Prayagraj", "Ghaziabad", "Bareilly",
    "Aligarh", "Moradabad", "Gorakhpur", "Noida (Gautam Buddha Nagar)", "Jhansi", "Saharanpur",
  ],
  "Madhya Pradesh": [
    "Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar", "Rewa", "Satna", "Ratlam",
    "Dewas", "Khandwa", "Chhindwara",
  ],
  "Bihar": [
    "Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga", "Purnia", "Nalanda", "Begusarai",
    "Munger", "Saharsa",
  ],
  "West Bengal": [
    "Kolkata", "Howrah", "North 24 Parganas", "South 24 Parganas", "Nadia", "Murshidabad",
    "Paschim Bardhaman", "Purba Bardhaman", "Darjeeling", "Jalpaiguri", "Malda",
  ],
  "Punjab": [
    "Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Hoshiarpur",
    "Ferozepur", "Moga", "Sangrur",
  ],
  "Haryana": [
    "Gurugram", "Faridabad", "Panipat", "Ambala", "Karnal", "Hisar", "Rohtak", "Sonipat",
    "Yamunanagar", "Panchkula",
  ],
  "Odisha": [
    "Khordha (Bhubaneswar)", "Cuttack", "Puri", "Sambalpur", "Rourkela (Sundargarh)", "Ganjam",
    "Balasore", "Mayurbhanj", "Kalahandi",
  ],
  "Assam": [
    "Kamrup (Guwahati)", "Dibrugarh", "Jorhat", "Silchar (Cachar)", "Tezpur (Sonitpur)",
    "Nagaon", "Tinsukia", "Barpeta",
  ],
  "Jharkhand": [
    "Ranchi", "Jamshedpur (East Singhbhum)", "Dhanbad", "Bokaro", "Hazaribagh", "Deoghar", "Giridih",
  ],
  "Chhattisgarh": [
    "Raipur", "Bilaspur", "Durg", "Korba", "Bastar (Jagdalpur)", "Rajnandgaon", "Raigarh",
  ],
  "Uttarakhand": [
    "Dehradun", "Haridwar", "Nainital", "Udham Singh Nagar", "Almora", "Pauri Garhwal",
  ],
  "Himachal Pradesh": [
    "Shimla", "Kangra", "Mandi", "Solan", "Una", "Hamirpur", "Kullu",
  ],
  "Jammu and Kashmir": [
    "Srinagar", "Jammu", "Baramulla", "Anantnag", "Udhampur", "Kathua",
  ],
  "Goa": ["North Goa", "South Goa"],
  "Tripura": ["West Tripura", "Gomati", "South Tripura", "North Tripura"],
  "Meghalaya": ["East Khasi Hills", "West Garo Hills", "Ri Bhoi"],
  "Manipur": ["Imphal East", "Imphal West", "Thoubal"],
  "Nagaland": ["Kohima", "Dimapur", "Mokokchung"],
  "Mizoram": ["Aizawl", "Lunglei"],
  "Arunachal Pradesh": ["Papum Pare (Itanagar)", "East Siang", "West Kameng"],
  "Sikkim": ["East Sikkim", "West Sikkim", "North Sikkim", "South Sikkim"],
  "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi"],
  "Chandigarh": ["Chandigarh"],
  "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"],
  "Ladakh": ["Leh", "Kargil"],
  "Andaman and Nicobar Islands": ["South Andaman", "North and Middle Andaman", "Nicobar"],
};

export const INDIAN_STATES = Object.keys(INDIA_LOCATIONS).sort();

export function getDistricts(state) {
  return INDIA_LOCATIONS[state] || [];
}

export default INDIA_LOCATIONS;
