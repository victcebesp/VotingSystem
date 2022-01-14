// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./../interfaces/IERC1155.sol";

contract VotingSystem {

    Proposal[] proposals;
    uint256 public proposalsAmount;
    address owner;
    IERC1155 collectionContract;
    // proposalId => tokenId => answer
    mapping(uint256 => mapping(uint256 => uint256)) usersProposalsAnswersByTokenId;
    Option[] private options;
    Option private option;
    Proposal private proposal;

    struct Proposal {
        uint256 id;
        bool isOpen;
        string description;
        Option[] options;
    }

    struct Option {
        string text;
        uint256 votes;
    }

    constructor(address _collectionContractAddress) {
        proposalsAmount = 0;
        owner = msg.sender;
        collectionContract = IERC1155(_collectionContractAddress);
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function addProposal(bool _isOpen, string memory _description, string[] memory _optionTexts) public onlyOwner {
        require(_optionTexts.length > 0);
        for(uint256 i = 0; i < _optionTexts.length; i++) {
            option.text = _optionTexts[i];
            option.votes = 0;
            options.push(option);
        }
        proposal.id = proposals.length;
        proposal.isOpen = _isOpen;
        proposal.description = _description;
        proposal.options = options;

        proposals.push(proposal);
        proposalsAmount += 1;
        delete options;
    }

    function getProposal(uint256 _proposalId) external view returns(Proposal memory) {
        require(_proposalId >= 0 && _proposalId < proposals.length,
            "Could not found proposal with such id");
        return proposals[_proposalId];
    }

    function getAllProposals() public view returns(Proposal[] memory) {
        return proposals;
    }

    function getUserAnswerForProposal(uint256 _proposalId, uint256 _tokenId) external view returns(uint256) {
        require(_proposalId >= 0 && _proposalId < proposals.length,
            "Could not found proposal with such id");
        return usersProposalsAnswersByTokenId[_proposalId][_tokenId];
    }

    function isCollector(address _sender, uint256 _tokenId) internal view returns(bool) {
        uint256 balance = collectionContract.balanceOf(_sender, _tokenId);
        return balance > 0;
    }

    function vote(uint256 _proposalId, uint256 _answer, uint256 _tokenId) external {
        require(_proposalId >= 0 && _proposalId < proposals.length,
            "Could not found proposal with such id");
        require(proposals[_proposalId].isOpen,
            "Proposal is not longer open to new votes");
        require(_answer != 0, "Voted option cannot be 0");
        require(_answer <= proposals[_proposalId].options.length, 
            "Voted option cannot be greater than the number of options");
        require(usersProposalsAnswersByTokenId[_proposalId][_tokenId] == 0, 
            "The token has already been used to vote");
        require(isCollector(msg.sender, _tokenId),
            "Only the user that owne this token can use it to vote");

        proposals[_proposalId].options[_answer - 1].votes += 1;
        usersProposalsAnswersByTokenId[_proposalId][_tokenId] = _answer;
    }

    function openProposal(uint256 _proposalId) external onlyOwner {
        require(_proposalId >= 0 && _proposalId < proposals.length,
            "Could not found proposal with such id");
        proposals[_proposalId].isOpen = true;
    }

    function closeProposal(uint256 _proposalId) external onlyOwner {
        require(_proposalId >= 0 && _proposalId < proposals.length,
            "Could not found proposal with such id");
            proposals[_proposalId].isOpen = false;
    }

}