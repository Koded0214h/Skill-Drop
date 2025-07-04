# Skill Drop

Skill Drop is a full-stack application that leverages blockchain technology to issue and manage skill-based NFTs. The project is organized into three main components: backend, frontend, and smart-contracts.

## Project Structure

```
root/
├── backend/           # API, server logic, and database
├── frontend/          # User interface (web app)
├── smart-contracts/   # Blockchain contracts and scripts
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
└── ...                # Other configuration and support files
```

## Components

### Backend
- Handles API requests, authentication, and business logic
- Manages data storage and communication with the blockchain
- Contains environment files for sensitive configuration

### Frontend
- Provides a user-friendly web interface
- Allows users to interact with the platform, view and claim NFTs, and manage their profiles
- Built with modern web technologies (React, Next.js, or similar)

### Smart Contracts
- Contains Solidity contracts for NFT minting and management
- Includes scripts for deployment and testing
- Uses Hardhat for development and testing

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <project-root>
   ```
2. **Install dependencies:**
   - For each component (backend, frontend, smart-contracts), run:
     ```bash
     cd <component-folder>
     npm install
     ```
3. **Set up environment variables:**
   - Copy `.env.example` to `.env` in each component and fill in required values.
4. **Run the project:**
   - Start backend, frontend, and blockchain nodes as described in their respective READMEs.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. 